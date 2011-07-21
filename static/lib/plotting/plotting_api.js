var debug = true;
var prevtype = null;
var types = { lin: {
                incr: function(i, step) { return i + step; },
                step: function(min,max,n) { return (max-min)/n; },
                index: function(value,min,step) { return Math.floor((value-min)/step); },
                dist: function(r,min,max) { return min + (max - min) * r; },
              },
              log: {
                incr: function(i, step) { return Math.exp(Math.log(i) + Math.log(step)); },
                step: function(min,max,n) { return Math.exp((Math.log(max)-Math.log(min))/n); },
                index: function(step,min,value) { return Math.floor(Math.log((value/min)/step)); },
                dist: function(r,min,max) { return Math.exp(Math.log(min) + Math.log(max / min) * r); },
              }
            };
var plots = [];
var stage = 1;
function DataSeries(props) {
  props.matrixfy = function(format) {
    return matrixfy(this.dims, this.func, format);
  }
  props.points = props.matrixfy(1);
  props.zs = props.matrixfy(3);
  return props;
}


var arrayMax = function( array ){
    var max = array[0];
    for (var i = 0; i < array.length; i ++)
      if (max < array[i])
        max = array[i];
    return max;
    //return Math.max.apply( Math, array );
};
var arrayMin = function( array ){
    var min = array[0];
    for (var i = 0; i < array.length; i ++)
      if (min > array[i])
        min = array[i];
    return min;
    //return Math.min.apply( Math, array );
};
function array_to_rgb(array) {
  return 'rgb(' + array[0] + ',' + array[1] + ',' + array[2] + ')';
}
function edges(data,type,n,min,max) {
  //var edges_ = [];
  if (min == undefined) min = arrayMin(data);
  if (max == undefined) max = arrayMax(data);
  if (min == max) max += 1;
  var step = types[type].step(min,max,n);
  //console.log(min,max,step);
  //for (var i = min; i < max; i = types[type].incr(i, step))
  //  edges_.push(i);
  return sortedindexify({ type: type, min: min, max: max, n: n, step: step }); //, edges_: edges_ };
}
function sortedindexify(o) {
  o.sortedindex = function(value) { return sortedindex(this, value); };
  return o;
}
function sortedindex(edges_, value) {
  var sortedindex = types[edges_.type].index(value, edges_.min, edges_.step);
  // If data falls off the top or bottom of the scale (i.e., if value is infinite)
  if (sortedindex >= edges_.n) return 1 * edges_.n;
  if (isNaN(sortedindex) || sortedindex < 0) return 0;
  return sortedindex;
}
function searchsorted(array, value, dir, at) {
  if (dir != 'right') dir = 'left';
  //console.log('i v c !at');
  
  for (var i = 0, compare; i < array.length; i ++) {
    compare = (!at && at !== 0) ? array[i] : array[i][at];
    //console.log(i, value, compare, !at && at !== 0);
    
    if (dir == 'left') {
      if (value <= compare)
        break;
    }
    else {
      if (value < compare)
        break;
    }
  }
  //console.log('value:', value,', compare:',compare.toFixed(3),', i:',i);
  return i;
}
function scale_min_floor(array, scalar) {
  for (var i = 0; i < array.length; i ++) {
    array[i] = Math.floor(scalar * Math.min(1, array[i]));
  }
  return array;
}




function Matrix(m) {
  m.cols = m[0].length;
  m.rows = m.length;
  m.autodims = { xmin: 0, xmax: m.cols, dx: 1, ymin: -1, ymax: m.rows - 1, dy: 1 };
  m.at = function(x, y) { return m[m.rows-y-1][x]; };
  m.matrixfy = function(format) { return matrixfy(m.autodims, m.at, format); };
  return m;
}
function matrixfy(d, func, format) {
  var matrix = [];
  for (var y = d.ymax; y > d.ymin; y -= d.dy) {
    var row = [];
    for (var x = d.xmin; x < d.xmax; x += d.dx) {
      switch (format) {
        case 1: row.push([x, y, func(x,y)]); break;
        case 2:
        case 3: row.push(func(x,y)); break;
      }
    }
    switch (format) {
      case 1:
      case 3: matrix.push.apply(matrix, row); break;
      case 2: matrix.push(row); break;
    }
  }
  return matrix;
}



function renderData(data, plotid, plot) {
    var m = Matrix(data.z);
    data = [ DataSeries({
        title: data.title,
        func: m.at,
        axis: "lin",
        dims: m.autodims,
        palette: "jet",
        edges: 255,
    }) ];

  var series = [];
  var options = { title: data[0].title, series: [], axes: { xaxis: { label: data[0].xlabel, tickOptions: { formatString: '%.2f' } }, yaxis: { label: data[0].ylabel, tickOptions: { formatString: '%.2f' } } }, cursor: { show: true, zoom: true, showTooltipDataPosition: true, showVerticalLine: true, showHorizontalLine: true, tooltipFormatString:  '%s (%s, %s, %s)' } };
  
  for (var index = 0; index < data.length; index ++) {
//    data[index].points = matrixfy(
    var s_ = data[index].points;
    var n  = data[index].edges;
    var edges_ = edges(data[index].zs,data[index].axis,n);
    data[index].edges_ = edges_;
    var palette = palettes[data[index].palette](n+1);
    data[index].palette_ = palette;
    //jQuery('#funcs').val(data[index].name);
    jQuery('#palettes').val(data[index].palette);
    jQuery('#numedges').val(data[index].edges);
    var resguess = Math.pow(2, Math.log((data[index].dims.xmax - data[index].dims.xmin) / data[index].dims.dx) / Math.log(2));
    jQuery('#res').val(resguess);
    //console.log(edges_.edges_);
    if (debug)
        console.log('palette.array.length: ', palette.array.length);
    
    for (var i = 0; i < s_.length; i ++) {
      //This is slow:
      //var sortedindex1 = searchsorted(edges_.edges_, data[index].zs[i]);
      var sortedindex2 = edges_.sortedindex(data[index].zs[i]);
      //To compare if we compute the same sortedindex using each method:
      //console.log(data[index].zs[i], sortedindex2);
      s_[i][2] = data[index].zs[i];
      s_[i][3] = { color: palette.str[sortedindex2] };
      s_[i][4] = palette.array[sortedindex2];
    }
    series.push(s_);
    //options.axes = { xaxis: { renderer: jQuery.jqplot.LogAxisRenderer, tickDistribution: 'power', tickOptions: { formatString: '%.0e' } } , yaxis: { renderer: jQuery.jqplot.LogAxisRenderer, tickDistribution: 'power', tickOptions: { formatString: '%.0e' } }};
    options.series.push({ renderer: jQuery.jqplot.pcolorRenderer, rendererOptions: { invisid: plotid.substring(0, plotid.length - 7) + '_invis', points: data[index].points, dims: data[index].dims, autoscaleBubbles: false, /*bodyWidth: 1, wickColor: 'red', openColor: 'yellow', closeColor: 'blue'*/ } });
    renderColorbar(plotid.substring(0, plotid.length - 7) + '_colorbar', palette, edges_, 13);
  }
  if (debug) {
      console.log('series: ', series);
      //console.log(options);
      console.log('stage: ', stage);
  }
  if (stage == 1) {
    plot = jQuery.jqplot(plotid, series, options);
    stage = 2;
  }
  else {
    for (i in series)
      plot.series[i].data = series[i];
    plot.options = options;
    plot.replot();
  }
  //plot = jQuery.jqplot(plotid, [[1,1]], {});
  return plot;

}
function colorbar(canvasid, palette) {
  var cvs = document.getElementById(canvasid);
  var ctx = getContext(canvasid);
  if (debug) {
      console.log('canvasid: ', canvasid);
      console.log('palette: ', palette);
  }
  cvs.height = palette.array.length;
  
  var imgd = ctx.createImageData(1, palette.array.length);
  var pix = imgd.data;
  for (var i = 0; n = pix.length, i < n; i += 4) {
    var rgba = palette.array[palette.array.length - 1 - i/4];
    pix[i] = rgba[0];
    pix[i+1] = rgba[1];
    pix[i+2] = rgba[2];
    pix[i+3] = 255;
  }
  ctx.putImageData(imgd, 0, 0);
  return imgd;
}
function renderColorbar(canvasid, palette, edges, nlabels) {
  var imgd = colorbar(canvasid + '_invis', palette);
  img2 = canvas2img(canvasid + '_invis');

  var cvs = document.getElementById(canvasid);
  var ctx = getContext(canvasid);
  img2.onload = function() {
      ctx.clearRect(0, 0, cvs.width, cvs.height);
      ctx.drawImage(this, 0, 0, 1, palette.array.length, 48, 11.5, cvs.width, cvs.height - 23);
  
      ctx.textBaseline = 'middle';
      ctx.textAlign = 'right';
      ctx.strokeStyle = '#666';
      ctx.fillStyle = '#666';
      ctx.beginPath();
      for (var i = 0; i <= nlabels - 1; i ++) {
        var r = i / (nlabels - 1);
        var val = types[edges.type].dist(r, edges.min, edges.max);
        var h = types.lin.dist(1 - r, 12, cvs.height - 12);
        ctx.fillText(val.toPrecision(3), 40, h + 1);
        ctx.moveTo(48, h + .5);
        ctx.lineTo(44, h + .5);
      }
      ctx.stroke();
  };
}
function test(canvasid, series) {
  var dims = series.dims;
  var w = Math.ceil((dims.xmax-dims.xmin)/dims.dx), h = Math.ceil((dims.ymax-dims.ymin)/dims.dy);
  var cvs = document.getElementById(canvasid);
  cvs.width = w; cvs.height = h;
  
  //var ctx = plot.grid._ctx;
  var ctx = getContext(canvasid);

  if (!series.points) series.points = series._plotData;

  var imgd = ctx.createImageData(w,h);
  var pix = imgd.data;
  for (var i = 0; n = pix.length, i < n; i += 4) {
  a=[i,n,w,h,dims];
    var rgba = series.points[i/4][4];
    pix[i] = rgba[0];
    pix[i+1] = rgba[1];
    pix[i+2] = rgba[2];
    pix[i+3] = 255;
  }
  x=imgd;
  ctx.putImageData(imgd, 0, 0);
  return imgd;
}
function getContext(id) {
  var elem = document.getElementById(id);
  if (!elem || !elem.getContext) {
    return;
  }

  // Get the canvas 2d context.
  var context = elem.getContext('2d');
  if (!context) {
    return;
  }
  return context;
}
function canvas2img(canvasid) {
  var cvs = document.getElementById(canvasid);
  var img = new Image();
  img.src = cvs.toDataURL('image/png');
  return img;
}


plotdata1 = {
    'type': '1d',
    'x': {'linear': {'data':[1,2,3,4], 'label':'position (m)'}},
    'y': [{
        'linear': {'data': [1,10,100,1000], 'label':'TbFe Intensity (cps)'},
        'log10': {'data': [0,1,2,3], 'label':'Log10 (TbFe Intensity (cps))'},
        }],
    'title': 'I am the title of the graph',
    'clear_existing': false,
    'color': 'Red',
    'style': 'line',
};
plotdata2 = {
    'type': '2d',
    'z':  [ [1, 2, 3, 4], [2, 3, 4, 1], [4, 1, 2, 3], [3, 4, 1, 2] ],
    'title': 'This is the title',
    'dims': {
      'xmax': 1.0,
      'xmin': 0.0, 
      'ymin': 0.0, 
      'ymax': 12.0,
      'xdim': 4,
      'ydim': 4,
    },
    'xlabel': 'This is my x-axis label',
    'ylabel': 'This is my y-axis label',
    'zlabel': 'This is my z-axis label',
};

function createPlotObject(plotid) {
    return { stage: 1, prevtype: null, targetId: plotid + '_target', series: [], options: { title: '', series: [], axes: {} } };
}
function plottingAPI(toPlots, plotid_prefix) {
    if (toPlots.constructor != Array)
        toPlots = [toPlots];
        // throw "Unsupported data format! Data must be a list of series.";
   // toPlots = $A(toPlots).flatten();

    for (var i = 0; i < toPlots.length; i ++) {
        var toPlot = toPlots[i];
        var plotid = plotid_prefix + '_' + i;
        var plot = (!plots[i]) ? createPlotObject(plotid) : plots[i];
        if (plot.prevtype != toPlot.type) plot.stage = 1;
        
        
        console.log(i, toPlot, toPlot.type, plot);
        switch (toPlot.type) {
            case '2d':
                document.getElementById('plots').appendChild(create2dPlotRegion(plotid));
                
                plot = renderData(toPlot, plotid + '_target', plot);
                jQuery(document.getElementById(plotid + '_selecty')).append('<option />', { value: toPlot.ylabel, text: toPlot.ylabel });
                jQuery(document.getElementById(plotid + '_selectx')).append('<option />', { value: toPlot.xlabel, text: toPlot.xlabel });
                break;
            case 'nd':
                document.getElementById('plots').appendChild(createNdPlotRegion(plotid));

                updateSeriesSelects(toPlot, plotid);
                plot = updateNdPlot(plot, toPlot, stage);
                
                jQuery(document.getElementById(plotid + '_update')).click({ plot: plot, toPlot: toPlot }, function(e) {
                    console.log(e);
                    var plot = e.data.plot; var toPlot = e.data.toPlot;
                    plot = updateNdPlot(plot, toPlot);
                });
            
            
                break;
            case '1d':
                var axis = "linear";
                if (toPlot.x[axis].data.length != toPlot.y[0][axis].data.length)
                    throw "Your data sucks";
                zipped = [];
                for (i in toPlot.x[axis].data)
                    if (!isNaN(toPlot.x[axis].data[i]))
                        zipped.push([toPlot.x[axis].data[i], toPlot.y[0][axis].data[i]]);
                if (debug)
                    console.log('zipped: ', zipped);


                if (! plotCreated || prevtype != '1d') {
                  plot = jQuery.jqplot(plotid, [zipped]);
                  plotCreated = true;
                }
                else {
                  plot.resetAxesScale();
                  plot.series[0].data = zipped;
                  plot.replot();
                }
                break;
                
            default:
                throw "Unsupported plot type! Please specify the type as '1d' or '2d'.";
        }
        
        prevtype = toPlot.type;
        console.log(123);
        plots[i] = plot;
        console.log(1234);
        
        /* 
        if (toPlot.x.length != toPlot.y.length)
          throw "Your data sucks";
        for (i in toPlot.x)
          if (!isNaN(toPlot.x[i]))
            zipped.push([toPlot.x[i], toPlot.y[i]]);


        if (! plotCreated) {
          plot=jQuery.jqplot(plotid, [zipped]);
          plotCreated = true;
          }
        else {
          plot.resetAxesScale();
          plot.series[0].data = zipped;
          plot.replot();
        }
        */
    }
}
function createNdPlotRegion(plotid, renderTo) {
    var div = document.createElement('div');
    div.setAttribute('id', plotid);
    div.setAttribute('class', 'plot-region');
    var divy = document.createElement('div');
    divy.setAttribute('id', plotid + '_divy');
    divy.setAttribute('class', 'plot-axis plot-axis-y');
    var divx = document.createElement('div');
    divx.setAttribute('id', plotid + '_divx');
    divx.setAttribute('class', 'plot-axis plot-axis-x');
    var divc = document.createElement('div');
    divc.setAttribute('id', plotid + '_divc');
    divc.setAttribute('class', 'plot-axis plot-axis-c');
    var divtarget = document.createElement('div');
    divtarget.setAttribute('id', plotid + '_target');
    divtarget.setAttribute('class', 'plot-target');
    var selecty = document.createElement('select');
    selecty.setAttribute('id', plotid + '_selecty');
    selecty.setAttribute('class', 'plot-axis-select plot-axis-select-y');
    var selectx = document.createElement('select');
    selectx.setAttribute('id', plotid + '_selectx');
    selectx.setAttribute('class', 'plot-axis-select plot-axis-select-x');
    var updatebutton = document.createElement('input');
    updatebutton.setAttribute('id', plotid + '_update');
    updatebutton.setAttribute('type', 'submit');
    updatebutton.setAttribute('value', 'Update plot');
    
    divy.appendChild(selecty);
    divx.appendChild(selectx);
    divx.appendChild(updatebutton);
    div.appendChild(divy);
    div.appendChild(divtarget);
    div.appendChild(divc);
    div.appendChild(divx);
    
    return div;
}
function updateSeriesSelects(toPlot, plotid) {
    //var plotid = plot.targetId.substring(1 * (plot.targetId[0] == '#'), plot.targetId.length - 7);
    
    var selectx = document.getElementById(plotid + '_selectx'),
        selecty = document.getElementById(plotid + '_selecty');
    var orders = { 'orderx': selectx, 'ordery': selecty };
    
    for (var order in orders) {
        for (var i = 0; i < toPlot[order].length; i ++) {
            var quantity = toPlot[order][i];
            var key = quantity.key || quantity;
            var label = quantity.label || quantity;
            
            // Make sure that each series defines data for this quantity
            for (var s = 0; s < toPlot.series.length; s ++) {
                if (!toPlot.series[s].data.hasOwnProperty(key))
                    throw "Quantity '" + key + "' is undefined in series '" + toPlot.series[s].label + "', but is expected from '" + order + "'";
            }
            // Append a new <option> for this quantity to the <select> element
            jQuery(orders[order]).append(jQuery('<option />', { value: key, text: label }));
        }
    }
}

function get(arr, i) {
    if (arr) {
        return arr[i];
    }
    else {
        return null;
    }
}

function updateNdPlot(plot, toPlot, stage) {
    var plotid = plot.targetId.substring(1 * (plot.targetId[0] == '#'), plot.targetId.length - 7);
    var series = plot.series;
    var options = plot.options;
    console.log(100, plotid, plot.series, toPlot);
    
    var quantityx = document.getElementById(plotid + '_selectx').value,
        quantityy = document.getElementById(plotid + '_selecty').value;
    console.log(200, plotid+'_selectx', quantityx, quantityy);
    
    for (var s = 0; s < toPlot.series.length; s++) {
        // Prototype.js's Enumerable.zip() is handy here
        var datax = toPlot.series[s].data[quantityx],
            datay = toPlot.series[s].data[quantityy];
        console.log(300, toPlot.series[s], quantityx, quantityy, datax, datay);
        // I know, I know: "series" is both singular and plural... go blame the English language, not me!
        //var serie = $A(datax.values).zip(datay.values, datax.errors, datay.errors, function(a) { return [a[0], a[1], { xerr: a[2], yerr: a[3] }]; });
        var serie = new Array();
        for (var i = 0; i < datax.values.length; i++) {
            serie[i] = [datax.values[i], datay.values[i], {xerr: get(datax.errors, i), yerr: get(datay.errors, i)}];
        }
        
        console.log('serie '+s, serie);
        if (!series[s] || !series[s].hasOwnProperty('data'))
            series[s] = serie;
        else
            series[s].data = serie;
        
        //options.series[s] = { renderer: jQuery.jqplot.errorbarRenderer, rendererOptions: { errorBar: true, /*bodyWidth: 1, wickColor: 'red', openColor: 'yellow', closeColor: 'blue'*/ } };
    }
    console.log('series', series, 'options', options);
    
    if (plot.stage == 1) {
        plot = jQuery.jqplot(plot.targetId, series, options);
    }
    else {
        plot.series.data = series;
        plot.options = options;
        plot.resetAxesScale();
        plot.replot();
    }
    return plot;
}

function create2dPlotRegion(plotid, renderTo) {
    var div = document.createElement('div');
    div.setAttribute('id', plotid);
    div.setAttribute('class', 'plot-region');
    var divy = document.createElement('div');
    divy.setAttribute('id', plotid + '_divy');
    divy.setAttribute('class', 'plot-axis plot-axis-y');
    var divx = document.createElement('div');
    divx.setAttribute('id', plotid + '_divx');
    divx.setAttribute('class', 'plot-axis plot-axis-x');
    var divc = document.createElement('div');
    divc.setAttribute('id', plotid + '_divx');
    divc.setAttribute('class', 'plot-axis plot-axis-c');
    var divtarget = document.createElement('div');
    divtarget.setAttribute('id', plotid + '_target');
    divtarget.setAttribute('class', 'plot-target');

    var selecty = document.createElement('select');
    selecty.setAttribute('id', plotid + '_selecty');
    selecty.setAttribute('class', 'plot-axis-select plot-axis-select-y');
    var selectx = document.createElement('select');
    selectx.setAttribute('id', plotid + '_selectx');
    selectx.setAttribute('class', 'plot-axis-select plot-axis-select-x');
    var updatebutton = document.createElement('input');
    updatebutton.setAttribute('id', plotid + '_update');
    updatebutton.setAttribute('type', 'submit');
    updatebutton.setAttribute('value', 'Update plot');
    
    var colorbar = document.createElement('canvas');
    colorbar.setAttribute('width', 60);
    colorbar.setAttribute('height', 500);
    colorbar.setAttribute('id', plotid + '_colorbar');
    colorbar.setAttribute('class', 'plot-colorbar');
    var invis = document.createElement('canvas');
    invis.setAttribute('id', plotid + '_invis');
    invis.setAttribute('class', 'plot-invis');
    var colorbarinvis = document.createElement('canvas');
    colorbarinvis.setAttribute('width', 1);
    colorbarinvis.setAttribute('id', plotid + '_colorbar_invis');
    colorbarinvis.setAttribute('class', 'plot-invis plot-colorbar-invis');

    
    divy.appendChild(selecty);
    divx.appendChild(selectx);
    divx.appendChild(updatebutton);
    div.appendChild(divy);
    div.appendChild(divtarget);
    div.appendChild(colorbar);
    div.appendChild(divc);
    div.appendChild(divx);
    divc.appendChild(invis);
    divc.appendChild(colorbarinvis);
    
    return div;
}
