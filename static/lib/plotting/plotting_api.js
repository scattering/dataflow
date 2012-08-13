var debug = false;
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
var plot = null; // starting with just one plot.
var stage = 1;
var myInteractor = null;

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
    for (var i = 0; i < array.length; ++i)
      if (max < array[i])
        max = array[i];
    return max;
    //return Math.max.apply( Math, array );
};
var arrayMin = function( array ){
    var min = array[0];
    for (var i = 0; i < array.length; ++i)
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

function logTickFormatter(format, val) {
    var new_val = Math.exp(Math.log(10)*val)
    return $.jqplot.DefaultTickFormatter(format, new_val)
}


var imgd = null;
var plot2d = null;
var plot2d_colorbar = null;
var process_bin_data = false;

function renderImageColorbar2(parent_plot, plotid, cbar_options) {
    var options = {
        //cursor: {show: true, zoom: true},
        paddingLeft: 0,
        sortData: false,
        interactors: [{ type:'standard', name: 'standard'}],
        series: [ {shadow: false, padding: 0} ],
        grid: {shadow: false},
        seriesDefaults:{
            yaxis: 'y2axis',
            shadow: false,
            renderer:$.jqplot.colorbarRenderer,
            rendererOptions: { parent_plot: parent_plot }
        },
        axes:{ 
            xaxis:{ tickOptions: {show: false} },
            y2axis:{
                //label: 'Intensity',
                labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                tickOptions: {
                    formatString: "%.3g",
                    _styles: {left: 5},
                }
            }
        }
    }
    
    var cbar_options = cbar_options || {};
    jQuery.extend(true, options, cbar_options);
        
    if (!plot2d_colorbar) {
        plot2d_colorbar = $.jqplot('colorbar', [[1,1]], options); 
    }
    else { // the colorbar already exists - just link it to the new plot
        plot2d_colorbar.series[0].parent_plot = parent_plot;
    }
    return plot2d_colorbar
}

/*
axesDefaults: {
        show: false,    // wether or not to renderer the axis.  Determined automatically.
        min: null,      // minimum numerical value of the axis.  Determined automatically.
        max: null,      // maximum numverical value of the axis.  Determined automatically.
        pad: 1.2,       // a factor multiplied by the data range on the axis to give the
                        // axis range so that data points don't fall on the edges of the axis.
        ticks: [],      // a 1D [val1, val2, ...], or 2D [[val, label], [val, label], ...]
                        // array of ticks to use.  Computed automatically.
        numberTicks: undefined,
        renderer: $.jqplot.LinearAxisRenderer,  // renderer to use to draw the axis,
        rendererOptions: {},    // options to pass to the renderer.  LinearAxisRenderer
                                // has no options,
        tickOptions: {
            mark: 'outside',    // Where to put the tick mark on the axis
                                // 'outside', 'inside' or 'cross',
            showMark: true,
            showGridline: true, // wether to draw a gridline (across the whole grid) at this tick,
            markSize: 4,        // length the tick will extend beyond the grid in pixels.  For
                                // 'cross', length will be added above and below the grid boundary,
            show: true,         // wether to show the tick (mark and label),
            showLabel: true,    // wether to show the text label at the tick,
            formatString: '',   // format string to use with the axis tick formatter
        }
        showTicks: true,        // wether or not to show the tick labels,
        showTickMarks: true,    // wether or not to show the tick marks
    },
*/


function transformData(transform) {
    if (transform == 'log') {
        for (var i=0; i<this.series.length; i++) {
            var pd = this.series[i]._plotData;
            var d = this.data[i];
            for (var j=0; j<pd.length; j++) {
                pd[j][1] = d[j][1]>0 ? Math.log(d[j][1]) / Math.LN10 : null;
            }
        }
        this.axes.yaxis.resetScale();
        this.axes.yaxis.labelOptions.label = "Log10(" + this.options.axes.yaxis.label + ")";
        //this.axes.yaxis.renderer = new $.jqplot.LogAxisRenderer();
        this.replot();
    } else { // transform == 'lin'
        for (var i=0; i<this.series.length; i++) {
            var pd = this.series[i]._plotData;
            var d = this.data[i];
            for (var j=0; j<pd.length; j++) {
                pd[j][1] = d[j][1];
            }
        }
        this.axes.yaxis.resetScale();
        this.axes.yaxis.labelOptions.label = this.options.axes.yaxis.label;
        //this.axes.yaxis.renderer = new $.jqplot.LinearAxisRenderer();
        this.replot();
    }
    this.transform = transform;
}

function toggleLogLin() {
    if (this.transform == 'log') this.setTransform('lin');
    else if (this.transform == 'lin') this.setTransform('log');
}

function render1dplot(data, transform, plotid, plot_options) {
    
    var options = {
        title: data.title,
        seriesDefaults: {shadow: false, markerOptions: {shadow: false, size: 4}, breakOnNull:true},
        axes:{
          xaxis:{
            renderer: $.jqplot.LinearAxisRenderer,  // renderer to use to draw the axis,
            label: data.xlabel,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                formatString: "%.2g"
            }
          },
          yaxis:{
            renderer: (transform == 'log') ? $.jqplot.LogAxisRenderer : $.jqplot.LinearAxisRenderer,
            label: data.ylabel,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                formatString: "%.2g",
                // fix for ticks drifting to the left in accordionview!
                _styles: {right: 0},
            }
          }
        },
        cursor: {
            show: true,
            zoom: true,
            clickReset: true,
            tooltipLocation:'se',
            tooltipOffset: -60,
            useAxesFormatters: false,
        },
        legend: {
            show: true,
            parent: this,
            placement: 'outside',
            renderer: $.jqplot.InteractiveLegendRenderer
        },
        grid: {shadow: false},
        sortData: false,
        //interactors: [ {type: 'Rectangle', name: 'rectangle'} ],
        type: '1d'
    };
    
    jQuery.extend(true, options, data.options);
    jQuery.extend(true, options, plot_options);
    $('#'+plotid).empty();
    plot1d = $.jqplot(plotid, data.data, options);
    plot1d.type = '1d';
    function handleLegendClick(ev) {
        var series_num = ev.target.getAttribute('series_num') || 0;
        //var mplot = ev.data.plot;
        var mplot = plot1d;
        mplot.series[series_num].show = !mplot.series[series_num].show;
        mplot.replot();
        //$('.jqplot-table-legend-label').click({plot: plot1d}, handleLegendClick);
    }
    //$('.jqplot-table-legend-label').click({plot: plot1d}, handleLegendClick);
    plot1d.legend.handleClick = handleLegendClick;
       
    plot1d.setTransform = transformData
    plot1d.setTransform(transform);
    plot1d.toggleLogLin = toggleLogLin;
    return plot1d
};

function renderImageData2(data, transform, plotid, plot_options) {
    var plot_options = plot_options || {};
    var dims = data.dims;
    var display_dims = data.display_dims || dims; // plot_dims = data_dims if not specified
    function roundToNearest(val, dmax, dmin, ddim){
        // round a value to the nearest whole value in the range
         var step = (dmax - dmin) / (ddim - 1);
         var index = Math.floor((val - dmin) / step);
         return (index * step) + dmin;
    }

    display_dims.xmin = roundToNearest(display_dims.xmin, dims.xmax, dims.xmin, dims.xdim);
    display_dims.xmax = roundToNearest(display_dims.xmax, dims.xmax, dims.xmin, dims.xdim);
    display_dims.ymin = roundToNearest(display_dims.ymin, dims.ymax, dims.ymin, dims.ydim);
    display_dims.ymax = roundToNearest(display_dims.ymax, dims.ymax, dims.ymin, dims.ydim);
    
    var options = {
        title: data.title,
        renderer: $.jqplot.heatmapRender,
        seriesDefaults:{
            renderer:$.jqplot.heatmapRenderer,
            rendererOptions: {
                dims: data.dims,
                transform: transform
                },
        },
        series: [{showMarker:false, showLine:false, breakOnNull:true}],
        axes:{
          xaxis:{
            label: data.xlabel,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                formatString: "%.2g"
            }
          },
          yaxis:{
            label: data.ylabel,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                formatString: "%.2g",
                // fix for ticks drifting to the left in accordionview!
                _styles: {right: 0},
            }
          }
        },
        cursor: {
            show: true,
            zoom: true,
            clickReset: true,
            tooltipLocation:'se',
            tooltipOffset: -60,
            useAxesFormatters: false,
        },
        grid: {shadow: false},
        sortData: false,
        //interactors: [ {type: 'Rectangle', name: 'rectangle'} ],
        type: '2d'
    };

    jQuery.extend(true, options, plot_options);
    plot2d = $.jqplot(plotid, data.z, options);
    plot2d.type = '2d';
    return plot2d
};

function renderndplot(data, transform, plotid, plot_options) {
    
    var options = {
        title: data.title,
        seriesDefaults: {shadow: false, markerOptions: {shadow: false, size: 4}, breakOnNull:true},
        axes:{
          xaxis:{
            renderer: $.jqplot.LinearAxisRenderer,  // renderer to use to draw the axis,
            label: data.xlabel,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                formatString: "%.2g"
            }
          },
          yaxis:{
            renderer: (transform == 'log') ? $.jqplot.LogAxisRenderer : $.jqplot.LinearAxisRenderer,
            label: data.ylabel,
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                formatString: "%.2g",
                // fix for ticks drifting to the left in accordionview!
                _styles: {right: 0},
            }
          }
        },
        cursor: {
            show: true,
            zoom: true,
            clickReset: true,
            tooltipLocation:'ne',
            tooltipOffset: -40,
            useAxesFormatters: false,
        },
        legend: {
            show: true,
            parent: this,
            placement: 'outsideGrid',
            xoffset: 10,
            renderer: $.jqplot.InteractiveLegendRenderer
        },
        grid: {shadow: false},
        sortData: false,
        //interactors: [ {type: 'Line', name: 'line'} ],
        type: 'nd'
    };
    
    jQuery.extend(true, options, data.options);
    jQuery.extend(true, options, plot_options);
    
    //jQuery(plotid).empty(); // empty the jqplot div in the DOM. Seemed unnecessary. 7/17/2012
    plotnd = jQuery.jqplot(plotid, data.data, options);

    //replot clears old axes instead of having new axes rendered on top of old axes.
    plotnd.replot({resetAxes : true});  
    
    plotnd.setTransform = transformData
    plotnd.setTransform(transform);
    plotnd.toggleLogLin = toggleLogLin;
    plotnd.type = 'nd';
    return plotnd
};



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

function createPlotObject(plotid) {
    return { stage: 1, prevtype: null, targetId: plotid + '_target', series: [], options: { title: '', series: [], axes: {} } };
}

function make_metadata_table(metadata, numcols) {
    var numcols = numcols || 4;
    var new_table = document.createElement('table');
    var keys = Object.keys(metadata);
    var num_items = keys.length;
    for (var i=0; i<num_items; i+=numcols) {
        var row = new_table.insertRow(-1);
        for (var j=0; j<numcols; j++) {
            var index = i + j;
            if (index >= num_items) { break; }
            var key = keys[index];
            
            var value = metadata[key];
            var label = row.insertCell(-1);
            label.setAttribute('class', 'metadata-label');
            label.innerHTML=key;
            var entry = row.insertCell(-1);
            entry.setAttribute('class', 'metadata-value');
            entry.innerHTML=value;
        }
    }
    return new_table;
}

function update1dPlot(plot, toPlots, target_id, plotnum, plot_options) {
    if (!plot || !plot.hasOwnProperty("type") || plot.type!='1d'){
        var plotdiv = document.getElementById(target_id);
        plotdiv.innerHTML = "";
        jQuery(plotdiv).append(jQuery('<div />', {style:"display: block; width: 700px; height: 350px;", id:"plotbox"}));
        jQuery(document.getElementById('plotbox')).append(jQuery('<div />', {style:"float: left; width:550px; height: 350px; ", id:"plotgrid"}));
        jQuery(plotdiv).append(jQuery('<div />', {style:"display: block; width: 410px; height: 100px;", id:"plotbuttons"}));
        jQuery(plotdiv).append(jQuery('<div />', {id:"metadata", class:"slidingDiv"}));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<select />', {id:"plot_selectz"}));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<select />', {id:"plot_selectnum"}));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<a />', {href:"#", class:"show_hide"}).text("Show/hide metadata"));
        jQuery(document.getElementById('plot_selectz')).append(jQuery('<option />', { value: 'lin', text: 'lin' }));
        jQuery(document.getElementById('plot_selectz')).append(jQuery('<option />', { value: 'log', text: 'log' }));
        
        plot = null;
        plot1d = null;
    }
    
    var plotnum = plotnum || 0;
    var toPlot = toPlots[plotnum];
    var toPlots = toPlots;
    var transform = toPlot.transform || 'lin';
    if (toPlot.metadata) {
        var metadata_table = make_metadata_table(toPlot.metadata);
        document.getElementById('metadata').innerHTML = "";
        document.getElementById('metadata').appendChild(metadata_table);
        jQuery(".show_hide").show();
    } else {
        jQuery(".show_hide").hide();
    }  
    
    document.getElementById('plot_selectnum').innerHTML = "";
    for (var i=0; i<toPlots.length; i++) {
        var label = toPlots[i].options.title || '';
        jQuery(document.getElementById('plot_selectnum')).append(jQuery('<option />', { value: i, text: 'dataset: ' + i + " " + label }));
    }
    
    plot = render1dplot(toPlot, transform, 'plotgrid', plot_options);

    var selectedIndex;
    if ( transform == 'log') { selectedIndex = 1 }
    else { selectedIndex = 0 }
    document.getElementById('plot_selectz').selectedIndex = selectedIndex;
    
    // out with the old bindings
    jQuery('#plot_selectnum').unbind('change');
    jQuery('#plot_selectz').unbind('change');
    
    function onchange(e) {
        var selectz = document.getElementById('plot_selectz');
        var selectnum = document.getElementById('plot_selectnum');
        var transform = selectz[selectz.selectedIndex].value;
        var plotnum = selectnum[selectnum.selectedIndex].value;
        var toPlot = toPlots[plotnum];
        plot = render1dplot(toPlot, transform, 'plotgrid');
        if (toPlot.metadata) {
            var metadata_table = make_metadata_table(toPlot.metadata);
            document.getElementById('metadata').innerHTML = "";
            document.getElementById('metadata').appendChild(metadata_table);
        }
    }

    // new bindings
    jQuery('#plot_selectnum').change({}, onchange);
    jQuery('#plot_selectz').change({}, onchange);
    jQuery('#fix_aspect_ratio').change({}, onchange);
    jQuery('#aspect_ratio').change({}, onchange);
    
    return plot; 
}

function updateTas2dPlot(toPlot, toPlots, target_id, plotnum, plot_options) {
    // Setting intial interactor points to be within the data range but offset from the corners of the data
    var dims = toPlots[0].dims; 
    var xoffset = (dims.xmax - dims.xmin) / 8.0; //Arbitrarily offset by 1/8 of width
    var yoffset = (dims.ymax - dims.ymin) / 8.0; //Arbitrarily offset by 1/8 of height
    var xmin = dims.xmin + xoffset;
    var ymin = dims.ymin + yoffset;
    var xmax = dims.xmax - xoffset;
    var ymax = dims.ymax - yoffset;
    plot_options['interactors'] = [ {type: 'Segment', name: 'segment', xmin: xmin, ymin: ymin, xmax: xmax, ymax: ymax} ];
    plot_options['cursor'] = {
        show: true,
        zoom: false,
        clickReset: true,
        tooltipLocation:'se',
        tooltipOffset: -60,
        useAxesFormatters: false,
    };

    //Creates div to contain plot
    var plotdiv = document.getElementById('sliceplot');
    jQuery(plotdiv).append(jQuery('<div />', {style:"display: block; width: 550px; height: 350px;", id:"interactor_plotgrid"}));

    //updates plot just like ordinary 2d plots
    plot = update2dPlot(toPlot, toPlots, target_id, plotnum, plot_options);
    plot.type = 'tas_2d';

    //Creating slice plot from the segment interactor
    slicePlot = $.jqplot('interactor_plotgrid', [[1,2]], {
        cursor: {show: true, zoom: true},
        grid: {shadow: false}, 
        sortData: false, 
        series: [ {shadow: false, color: 'blue', markerOptions: {shadow: false, size: 4}} ],
        axesDefaults: {
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {formatString: "%.3g", _styles: {right: 0}}
        },
        axes: {xaxis: {label: plot.axes.xaxis.label}, yaxis: {label: 'detector counts'}}
    });

    //Creating drop-down to change x-axis for interactor plot
    //Creating div to indicate when the interactor plot is updating.
    jQuery(plotdiv).append(jQuery('<div />', {style:"display: block; width: 600px; height: 50px;", id:"interactorplotbuttons"}));
    jQuery(document.getElementById('interactorplotbuttons')).append(document.createTextNode('Choose x-axis: '));
    jQuery(document.getElementById('interactorplotbuttons')).append(jQuery('<select />', {id:"plot_select_xaxis"}));
    jQuery(document.getElementById('interactorplotbuttons')).append(jQuery('<div />', {style:"float: right; width: 300px; height: 25px; padding-top: 5px", id:"interactor_update_div", innerHTML: " Plot updated. Move interactor to update plot. "}));
    //NOTE: do NOT change ordering: x axis must be labeled first (based on success function of ajax request)
    jQuery(document.getElementById('plot_select_xaxis')).append(jQuery('<option />', { value: plot.axes.xaxis.label, text: plot.axes.xaxis.label }));
    jQuery(document.getElementById('plot_select_xaxis')).append(jQuery('<option />', { value: plot.axes.yaxis.label, text: plot.axes.yaxis.label }));
    //add listener for the x-axis select. 
    document.getElementById('plot_select_xaxis').addEventListener("change", selectHandler, false);
    


    myInteractor = plot.plugins.interactors.segment; //reference to the segment interactor
    var s1 = initialize_interactor_listeners(plot.series[0], toPlots[plotnum].original_data);
    s1.updateInteractorPlot(); //intially update the interactor to appropriately plot its initial location.

    return plot;
}

//If the interactor plot x-axis is changed, update the plot
selectHandler = function (event) {
    if (event.hasOwnProperty('type') && event.type == "change") {
        updateInteractorPlot();
    }
};

initialize_interactor_listeners = function(series, original_data) {
    //Setting up listeners for when the point is droped, ie mouse released
    var number_of_ajax_running = 0;

    myInteractor.p1.onDrop = function (e, pos) {
        updateInteractorPlot();
    };
    myInteractor.p2.onDrop = function (e, pos) {
        updateInteractorPlot();
    };
    myInteractor.segment.onDrop = function (e, pos) {
        updateInteractorPlot();
    };

    this.updateInteractorPlot = function() {
        // Setting inner HTML to indicate that plot is updating
        ++number_of_ajax_running;
        if (number_of_ajax_running > 0) 
            document.getElementById('interactor_update_div').innerHTML = " Updating Plot... ";

        $.ajax({
            url: '/calculateSlice/',
            type: 'GET',
            data: {'x1' : myInteractor.p1.coords.x, 'y1' : myInteractor.p1.coords.y, 'x2' : myInteractor.p2.coords.x, 'y2': myInteractor.p2.coords.y, 'xarr': Ext.encode(original_data.xarr), 'yarr': Ext.encode(original_data.yarr), 'zarr': Ext.encode(original_data.zarr)},
            success: function(response) {
                //on success, replots the interactor plot.
                var result = Ext.decode(response);
                var select_div = jQuery(document.getElementById('plot_select_xaxis'))[0];

                // selectedIndex=0 when x-axis is chosen; selectedIndex=1 when y-axis is chosen
                var x = result[select_div.selectedIndex ? 'line_y' : 'line_x'];
                var z = result['zout'];
                var xdata = [];
                for (var i = 0; i < x.length; ++i){
                    xdata.push([x[i], z[i]]);
                }

                slicePlot = $.jqplot('interactor_plotgrid', [xdata], {
                    cursor: {show: true, zoom: true},
                    grid: {shadow: false}, 
                    sortData: false, 
                    series: [ {shadow: false, color: 'blue', markerOptions: {shadow: false, size: 4}} ],
                    axesDefaults: {
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                        tickOptions: {formatString: "%.3g", _styles: {right: 0}}
                    },
                    axes: {xaxis: {label: select_div.value}, yaxis: {label: 'detector counts'}}
                });
                //slicePlot.axes.xaxis.label = select_div.value; //div configured so value = axis label
                slicePlot.replot({resetAxes : true});

                // Setting inner HTML to indicate that all queued plot ajax requests have finished
                --number_of_ajax_running;
                if (number_of_ajax_running < 1) {
                    document.getElementById('interactor_update_div').innerHTML = " Plot updated. Move interactor to update plot. ";
                }
            },
            failure: function(response) {
                alert('Segment point locations are invalid!');
            }
        });
    };
    return this;
};

function update2dPlot(plot, toPlots, target_id, plotnum, plot_options) {
    if (!plot || !plot.hasOwnProperty("type") || plot.type!='2d'){
        var plotdiv = document.getElementById(target_id);
        plotdiv.innerHTML = "";
        jQuery(plotdiv).append(jQuery('<div />', {style:"display: block; width: 700px; height: 350px;", id:"plotbox"}));
        jQuery(document.getElementById('plotbox')).append(jQuery('<div />', {style:"float: left; width:550px; height: 350px; ", id:"plotgrid"}));
        jQuery(document.getElementById('plotbox')).append(jQuery('<div />', {style:"float: left; width: 100; height: 350; ", id:"colorbar"}));
        jQuery(plotdiv).append(jQuery('<div />', {style:"display: block; width: 410px; height: 100px;", id:"plotbuttons"}));
        jQuery(plotdiv).append(jQuery('<div />', {id:"metadata", class:"slidingDiv"}));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<select />', {id:"plot_selectz"}));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<select />', {id:"plot_selectnum"}));
        jQuery(document.getElementById('plotbuttons')).append(document.createTextNode('Fix aspect ratio:'));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<input />', {id:"fix_aspect_ratio", type:"checkbox", checked: false}));
        jQuery(document.getElementById('plotbuttons')).append(document.createTextNode('value:'));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<input />', {id:"aspect_ratio", type:"text", value:"1.0", width: "45px"}));
        jQuery(document.getElementById('plotbuttons')).append(jQuery('<a />', {href:"#", class:"show_hide"}).text("Show/hide metadata"));
        //jQuery(document.getElementById('plotbuttons')).append(jQuery('<input />', {id:"plot_update", type:"submit", value:"Update plot"}));
        jQuery(document.getElementById('plot_selectz')).append(jQuery('<option />', { value: 'lin', text: 'lin' }));
        jQuery(document.getElementById('plot_selectz')).append(jQuery('<option />', { value: 'log', text: 'log' }));
        
        plot = null;
        plot2d = null;
        plot2d_colorbar = null;
    }
    
    var plotnum = plotnum || 0;
    var toPlot = toPlots[plotnum];
    var toPlots = toPlots;
    var transform = toPlot.transform || 'lin';
    var aspectRatio = toPlot.aspectRatio || 1.0;
    if (toPlot.metadata) {
        var metadata_table = make_metadata_table(toPlot.metadata);
        document.getElementById('metadata').innerHTML = "";
        document.getElementById('metadata').appendChild(metadata_table);
        jQuery(".show_hide").show();
    } else {
        jQuery(".show_hide").hide();
    }
    document.getElementById('aspect_ratio').value = aspectRatio;
    var fixAspect = toPlot.fixAspect || false;
    document.getElementById('fix_aspect_ratio').checked = fixAspect;    
    
    document.getElementById('plot_selectnum').innerHTML = "";
    for (var i=0; i<toPlots.length; i++) {
        var zlabel = toPlots[i].zlabel || '';
        jQuery(document.getElementById('plot_selectnum')).append(jQuery('<option />', { value: i, text: 'dataset: ' + i + " " + zlabel }));
    }
    
    jQuery.extend(true, plot_options, {'fixedAspect': {'fixAspect': fixAspect, 'aspectRatio': aspectRatio}});
    plot = renderImageData2(toPlot, transform, 'plotgrid', plot_options);
    colorbar = renderImageColorbar2(plot.series[0], 'colorbar');
    plot2d.series[0].zoom_to();
    plot2d.replot();
    var selectedIndex;
    if ( transform == 'log') { selectedIndex = 1 }
    else { selectedIndex = 0 }
    document.getElementById('plot_selectz').selectedIndex = selectedIndex;
    
    // out with the old bindings
    jQuery('#plot_selectnum').unbind('change');
    jQuery('#plot_selectz').unbind('change');
    
    function onchange(e) {
        var selectz = document.getElementById('plot_selectz');
        var selectnum = document.getElementById('plot_selectnum');
        var fixAspect = document.getElementById('fix_aspect_ratio').checked;
        var aspectRatio = document.getElementById('aspect_ratio').value;
        var transform = selectz[selectz.selectedIndex].value;
        var plotnum = selectnum[selectnum.selectedIndex].value;
        var toPlot = toPlots[plotnum];
        //plot = renderImageData2(toPlot, transform, 'plot2d');
        var new_dims = $.extend(true, {}, toPlot.dims);
        plot2d.series[0].set_data(toPlot.z[0], new_dims);
        colorbar.series[0].set_dims(new_dims);
        plot2d.series[0].set_transform(transform);
        plot2d.title.text = toPlot.title;
        plot2d.series[0].zoom_to();
        plot2d.plugins.fixedAspect.fixAspect = fixAspect;
        plot2d.plugins.fixedAspect.aspectRatio = aspectRatio;
        plot2d.replot();
        colorbar = renderImageColorbar2(plot.series[0], 'colorbar');
        if (colorbar.plugins._interactor) {
            colorbar.plugins._interactor.zoomMax();
        } else {
            colorbar.replot();
        }
        if (toPlot.metadata) {
            var metadata_table = make_metadata_table(toPlot.metadata);
            document.getElementById('metadata').innerHTML = "";
            document.getElementById('metadata').appendChild(metadata_table);
        }
    }

    // new bindings
    jQuery('#plot_selectnum').change({}, onchange);
    jQuery('#plot_selectz').change({}, onchange);
    jQuery('#fix_aspect_ratio').change({}, onchange);
    jQuery('#aspect_ratio').change({}, onchange);
//    jQuery('#plot_update').unbind('click');
//    jQuery('#plot_update').click({ plot: plot, colorbar: colorbar, toPlots: toPlots }, onchange
//        function(e) {
//            console.log(e);
//            var plot = e.data.plot; var toPlots = e.data.toPlots; var colorbar = e.data.colorbar;
//            var selectz = document.getElementById('plot_selectz');
//            var selectnum = document.getElementById('plot_selectnum');
//            var transform = selectz[selectz.selectedIndex].value;
//            var plotnum = selectnum[selectnum.selectedIndex].value;
//            var toPlot = toPlots[plotnum];
//            console.log('replot: ', plotnum, transform, toPlot, toPlots)
//            plot = renderImageData(toPlot, transform, 'plots');
//            colorbar = renderImageColorbar(toPlot, transform, 'colorbar');
//        }
//    );
    
    return plot; 
}

var plot = null;
var plotregion = null;
var toPlots_input = null;
var myndgridpanel = null;
var errorbarsOn = false; //true will turn errorbars on for ndplotting.

function plottingAPI(toPlots, plotid_prefix, plot_options) {
    // plot_options are passed to the individual plot renderers
    var plot_options = plot_options || {};
    $.jqplot.config.enablePlugins = true;
    toPlots_input = toPlots;
    if (debug) console.log(toPlots.constructor.name);
    if (!(Array.isArray(toPlots))) {
        toPlots = [toPlots];
        if (debug)
            console.log('changing singleton data to length-1 array')

        // throw "Unsupported data format! Data must be a list of series.";
    }
// toPlots = $A(toPlots).flatten();
    
    if (debug)
        console.log('toPlots:', toPlots)
    // assuming all plots in the list are of the same type!
    plot_type = toPlots[0].type
    
    switch (plot_type) {
        case 'tas_2d':
            plot = updateTas2dPlot(plot, toPlots, plotid_prefix, 0, plot_options);
            break;

        case '2d':
            plot = update2dPlot(plot, toPlots, plotid_prefix, 0, plot_options);
            break;
        
        case '1d':
            plot = update1dPlot(plot, toPlots, plotid_prefix, 0, plot_options);
            break;
        
        case 'nd': 
            var toPlot = toPlots;
            var plotid = plotid_prefix + '_nd';
            
            plot = updateNdPlot(plot, toPlot, plotid, plotid_prefix, true, plot_options); 
            //with create=true, myndgridpanel will be created and not null.

            //Listener for clicking the Toggle Errorbar button.
            jQuery(document.getElementById(plotid + '_toggle')).unbind('click');
            jQuery(document.getElementById(plotid + '_toggle')).click(
                function (e) {
                    var toPlot = getSelectedPlots();
                    errorbarsOn = !errorbarsOn; //toggle
                    plot = updateNdPlot(plot, toPlot, plotid, plotid_prefix, false, plot_options);
                }
            );
            // logscale
            jQuery(document.getElementById(plotid + '_toggleloglin')).unbind('click');
            jQuery(document.getElementById(plotid + '_toggleloglin')).click(
                function (e) {
                    if (plot && plot.toggleLogLin) plot.toggleLogLin();
                }
            );

            // Setting up auto-update when drop-down menu changes
            jQuery(document.getElementById(plotid + '_selectx')).change(
                function (e) {
                    var toPlot = getSelectedPlots();
                    plot = updateNdPlot(plot, toPlot, plotid, plotid_prefix, false, plot_options);
                }
            );
            jQuery(document.getElementById(plotid + '_selecty')).change(
                function (e) {
                    var toPlot = getSelectedPlots();
                    plot = updateNdPlot(plot, toPlot, plotid, plotid_prefix, false, plot_options);
                }
            );
            jQuery(document.getElementById(plotid)).keypress(
                function (e) {
                    console.log(e);
                    if (event.which == 108 || event.which == 76) {
                        if (plot && plot.toggleLogLin) plot.toggleLogLin();
                    }
                }
            );
            break;
        
        default:
            alert('plotting of datatype "' + plot_type + '" is unsupported');
    }
}

function getSelectedPlots(){
    toPlotArr = [];
    Ext.each(myndgridpanel.getSelectionModel().selected.items, function(item, i) {
        toPlotArr.push(item.data.toPlotObj);
    });
    return toPlotArr;
}


function makeNdPlotSelector(toPlot, plotid, plotid_prefix, plot_options) {
    /* Creates the plotgrid by instantiating the columns and store based on the passed objects
       Currently for ndplotting only. */
    //Creating store and grid.
    var storeFields = [{name: 'Files'}, {name: 'Legend'}, {name: 'toPlotObj'}];
    Ext.regModel('fileModel', {
        fields: storeFields
    });
    var store = Ext.create('Ext.data.Store', { model: 'fileModel'});

    
    var myCheckboxModel = new Ext.selection.CheckboxModel({
        listeners: {
            selectionchange: function(model, records) {
                //The update button is already handling this...
                //unless we want each check click to update plot                
                var recordToPlots = [];
                Ext.each(records, function(record, i){
                    recordToPlots.push(record.data.toPlotObj);
                });
                //plot = updateNdPlot(plot, recordToPlots, plotid, plotid_prefix, false);
                plot = updateNdPlot(plot, recordToPlots, 'plot_nd', 'plot', false, plot_options);
            }
        }
    });

    //add all files to the store..
    var filerecs=[];
    for (var j = 0; j < toPlot.length; ++j) {
        var filerec = {};
        filerec['Files'] = toPlot[j].series[0].label;
        //filerec['Legend'] = NaN;            //NaN for now... using jqplot's legend for now.
        filerec['toPlotObj'] = toPlot[j];   //hidden field
        filerecs.push(filerec);
    }

    //TODO setup renderer for 'Legend'
    var gridColumns = [];
    gridColumns.push({header: 'Files', width: 150, sortable: true, dataIndex: 'Files'});
    //gridColumns.push({header: 'Legend', hidden: true, sortable: false, dataIndex: 'Legend'});
    gridColumns.push({header: 'toPlotObj', hidden: true, sortable: false, dataIndex: 'toPlotObj'});
    store.loadData(filerecs);

    //select first file to plot by default
    var record = store.getRange()[0];
    myCheckboxModel.selected.add(record);


    /* GridPanel that displays the data. */
    var plotgridpanel = new Ext.grid.GridPanel({
        id: 'plotgridpanel',
        store: store,
        selModel: myCheckboxModel,
        columns: gridColumns,
        stripeRows: true,
        height: 410,
        width: 190,
        //autoWidth: true,
        title: 'Select the files to plot:',
        //renderTo: 'plot' //gridplotid,
    });

    return plotgridpanel;
}


function createNdPlotRegion(plotid, renderTo) {
    var div = document.createElement('div');
    div.setAttribute('id', plotid);
    //div.setAttribute('style', 'display: block; width: 550; height: 350;');
    div.setAttribute('class', 'plot-region');
    var divy = document.createElement('div');
    divy.setAttribute('id', plotid + '_divy');
    divy.setAttribute('class', 'plot-axis plot-axis-y');
    var divx = document.createElement('div');
    divx.setAttribute('id', plotid + '_divx');
    divx.setAttribute('class', 'plot-axis plot-axis-x');
    //var divc = document.createElement('div');
    //divc.setAttribute('id', plotid + '_divc');
    //divc.setAttribute('class', 'plot-axis plot-axis-c');
    var divtarget = document.createElement('div');
    divtarget.setAttribute('id', plotid + '_target');
    //divtarget.setAttribute('style', 'display: block; width: 450; height: 350;');
    divtarget.setAttribute('class', 'plot-target');
    var selecty = document.createElement('select');
    selecty.setAttribute('id', plotid + '_selecty');
    selecty.setAttribute('class', 'plot-axis-select plot-axis-select-y');
    var selectx = document.createElement('select');
    selectx.setAttribute('id', plotid + '_selectx');
    selectx.setAttribute('class', 'plot-axis-select plot-axis-select-x');
    var errorbartogglebutton = document.createElement('input');
    errorbartogglebutton.setAttribute('id', plotid + '_toggle');
    errorbartogglebutton.setAttribute('type', 'submit');
    errorbartogglebutton.setAttribute('value', 'Toggle Errorbars');
    var loglintogglebutton = document.createElement('input');
    loglintogglebutton.setAttribute('id', plotid + '_toggleloglin');
    loglintogglebutton.setAttribute('type', 'submit');
    loglintogglebutton.setAttribute('value', 'Toggle log/lin');


    divy.appendChild(selecty);
    divx.appendChild(selectx);
    divx.appendChild(errorbartogglebutton);
    divx.appendChild(loglintogglebutton);
    div.appendChild(divy);
    div.appendChild(divtarget);
    //div.appendChild(divc);
    div.appendChild(divx);
    
    return div;
}

function updateSeriesSelects(toPlot, plotid) {
    //var plotid = plot.targetId.substring(1 * (plot.targetId[0] == '#'), plot.targetId.length - 7);
    
    var selectx = document.getElementById(plotid + '_selectx'),
        selecty = document.getElementById(plotid + '_selecty');
    var orders = { 'orderx': selectx, 'ordery': selecty };
    
    for (var order in orders) {
        orders[order].innerHTML = ""
        for (var i = 0; i < toPlot[order].length; i ++) {
            var quantity = toPlot[order][i];
            var key = quantity.key || quantity;
            var label = quantity.label || quantity;
            
            // Make sure that each series defines data for this quantity
            for (var s = 0; s < toPlot.series.length; s ++) {
                if (!toPlot.series[s].data.hasOwnProperty(key))
                    throw "Quantity '" + key + "' is undefined in series '" + toPlot.series[s].label + "', but is expected from '" + order + "'";
            }
            if (debug) console.log("updating series selects", key,label);
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

function updateNdPlot(plot, toPlot, plotid, plotid_prefix, create, plot_options) {
    if (create || !plot || !plot.hasOwnProperty("type") || plot.type!='nd'){
        var plotdiv = document.getElementById(plotid_prefix);
        plotdiv.innerHTML = "";  //removing the "I am a plot." from plotwindow.html's div
        myplotdiv = createNdPlotRegion(plotid);  //creates plot div
        myndgridpanel = makeNdPlotSelector(toPlot, plotid, plotid_prefix, plot_options);  //creates gridpanel file selector
        
        myplotpanel = new Ext.panel.Panel({
            height: 410,
            //width: 565,
            flex: 1,
            //autoheight: true,
            contentEl: myplotdiv,
        });
        
        new Ext.panel.Panel({
            layout: {
                type: 'hbox',
                padding: 10
            },
            frame: true,
            //height: 600,
            autoheight: true,
            width: 800,
            //autowidth: true,
            renderTo: plotid_prefix, //'plot'
            //defaults: { flex: 1 },
            items: [ myndgridpanel, {xtype: 'splitter', width: 15}, myplotpanel ]
            
        });
        toPlot = [toPlot[0]] //only doing the first file (set up so first file is only one checked in gridpanel)
        updateSeriesSelects(toPlot[0], plotid);
    } 

    target_id = plotid + '_target';
    var series = new Array();
    var markerOptionsArray = ['filledSquare', 'circle', 'diamond', 'x'];
    var numberOptions = 4; // markerOptionsArray.length; //hardcoding for speed
    var markerIndex = 0;

    var quantityx = document.getElementById(plotid + '_selectx').value,
        quantityy = document.getElementById(plotid + '_selecty').value;

    toPlotlength = toPlot.length;

    var data = {};
    data.data = series;
    data.title = (toPlotlength > 0) ? toPlot[0].title : "Empty plot";
    data.options = {series: []}; // legend names/labels go in the 'series' option
    data.xlabel = quantityx;
    data.ylabel = quantityy;

    //recently added outer for - may not be necessary
    for (var p = 0; p < toPlotlength; ++p){
        toPlot_p = toPlot[p];
        for (var s = 0; s < toPlot_p.series.length; ++s) {
            // For TripleAxis plottables, this loop will only run once...  7/17/2012
            var datax = toPlot_p.series[s].data[quantityx],
                datay = toPlot_p.series[s].data[quantityy];
                filename = toPlot_p.series[s].label;

            // I know, I know: "series" is both singular and plural... 
            // go blame the English language, not me!
            // Prototype.js's Enumerable.zip() is handy here
            //var serie = $A(datax.values).zip(datay.values, datax.errors, datay.errors, function(a) { return [a[0], a[1], { xerr: a[2], yerr: a[3] }]; });

            // Following Ophir's 'serie/series' convention...
            var serie = new Array();
            if (datax.values) {
                for (var i = 0; i < datax.values.length; ++i) {
                    var xerror = get(datax.errors, i) / 2.0;
                    var yerror = get(datay.errors, i) / 2.0;
                    
                    serie[i] = [datax.values[i], datay.values[i], {xerr: [xerror, xerror], yerr: [yerror, yerror]}];
                }
            } else {
                //if the file does not have plotable data for the selected axes, 
                //just plot the origin to avoid jqplot errors.
                serie = [[0,0]];
            }

            series.push(serie);
            linestyle = markerOptionsArray[markerIndex % numberOptions];
            ++markerIndex;

            //if the errorbars are toggled on, add the errorbarRenderer. Otherwise do not.
            //markerOptions do not seem to render when errorbars are on. 7/20/2012
            data.options.series.push((errorbarsOn) ? {label: filename, renderer: $.jqplot.errorbarRenderer, rendererOptions: {errorBar: true}/*, markerOptions: {size: 5, style: linestyle}*/} : {label: filename, markerOptions: {size: 5, style: linestyle}});
            
            //data.options.series.push({label: filename, renderer: $.jqplot.errorbarRenderer, rendererOptions: {errorBar: true}});
        }
    }
    
    
    if (series.length == 0) {
        //if there are no files selected to plot, origin  and hide the legend.
        data.data = [[[0,0]]];
        data.options.legend = {show: false};
    }

    var transform = 'lin'; //For now, only setting to 'log' will set it. Defaults to linear
    plot = renderndplot(data, transform, target_id, plot_options);
    return plot;
}

function create2dPlotRegion(plotid, renderTo) {
    var div = document.createElement('div');
    div.setAttribute('id', plotid);
    div.setAttribute('class', 'plot-region');
//    var divy = document.createElement('div');
//    divy.setAttribute('id', plotid + '_divy');
//    divy.setAttribute('class', 'plot-axis plot-axis-y');
//    var divx = document.createElement('div');
//    divx.setAttribute('id', plotid + '_divx');
//    divx.setAttribute('class', 'plot-axis plot-axis-x');
//    var divc = document.createElement('div');
//    divc.setAttribute('id', plotid + '_divc');
//    divc.setAttribute('class', 'plot-axis plot-axis-c');
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
    updatebutton.setAttribute('value', 'Update plot ');
    
//    var colorbar = document.createElement('canvas');
//    colorbar.setAttribute('width', 60);
//    colorbar.setAttribute('height', 500);
//    colorbar.setAttribute('id', plotid + '_colorbar');
//    colorbar.setAttribute('class', 'plot-colorbar');
//    var invis = document.createElement('canvas');
//    invis.setAttribute('id', plotid + '_invis');
//    invis.setAttribute('class', 'plot-invis');
//    invis.hidden = true;
//    var colorbarinvis = document.createElement('canvas');
//    colorbarinvis.setAttribute('width', 1);
//    colorbarinvis.setAttribute('id', plotid + '_colorbar_invis');
//    colorbarinvis.setAttribute('class', 'plot-invis plot-colorbar-invis');
//    colorbarinvis.hidden = true;

    
    div.appendChild(selecty);
    div.appendChild(selectx);
    div.appendChild(updatebutton);
    //div.appendChild(divy);
    div.appendChild(divtarget);
    //div.appendChild(colorbar);
    //div.appendChild(divc);
    //div.appendChild(divx);
    //divc.appendChild(invis);
    //divc.appendChild(colorbarinvis);
    
    return div;
}

