var _fs = function(ks) {
  return function(i) { return jQuery.map(jQuery.map(ks, _f), function(f) { return f(i); }); };
};
var _f = function(k) {
  return function(i) { return k * i; };
};
var _mapify = function(rgbfunc) {
  return function(n) {
    var arraymap = [], strmap = [];
    for (var i = 0; i < n; i ++) {
      var array = scale_min_floor(rgbfunc(i / n), 255);
      var str = array_to_rgb(array);
      arraymap.push(array);
      strmap.push(str);
    }
    return { array: arraymap, str: strmap };
  };
};
var _h2rgb = function(h) {
  h = 4.8/6*(1-h);
  if(h<1/3.) {//         _    _
    r=(2-h*6)/2;  //   red: | \__/ |
    g=(h*6)/2;    //        0 __   1
    b=0;      // green: |/  \__|
  }else if(h<2/3.) { // 0   __ 1
    r=0;      //  blue: |__/  \|
    g=4-h*6;  //        0 |  | 1
    b=h*6-2;  //         1/3 2/3
  }else{
    r=(h*6-4)/2;
    g=0;
    b=((1-h)*6)/2;
  }
  if(r>1) r=1;
  if(g>1) g=1;
  if(b>1) b=1;
  return [r,g,b];
}
var Palettify = function(palettes) {
  for (i in palettes) {
    palettes[i] = _mapify(palettes[i]);
  }
  return palettes;
};
var palettes = Palettify({
  copper: _fs([1.25, 0.8, 0.5]),
  grey: _fs([1,1,1]),
  myjet: _h2rgb,
  jet: function(h) { return color_blend_segments(h, jet_segmentdata); },
  accent: function(h) { return color_blend_segments(h, accent_segmentdata); },
});
var numedges = { 1: '1 (Malevich)',3:'3 (choppiest)',7:7,15:15,31:31,63:63,127:127,255:255,511:'511 (smoothest)' };
var reses = [ 2, 4, 8, 16, 32, 64, 128, 256, 311 ];

function renderSelects(ids) {
  for (func in funcs)
    jQuery('#' + ids[0]).append(jQuery('<option />', { value: func, text: func }));
  for (palette in palettes)
    jQuery('#' + ids[1]).append(jQuery('<option />', { value: palette, text: palette }));
  for (numedge in numedges)
    jQuery('#' + ids[2]).append(jQuery('<option />', { value: numedge, text: numedges[numedge] }));
  for (res in reses)
    jQuery('#' + ids[3]).append(jQuery('<option />', { value: reses[res], text: reses[res] }));
  jQuery('#' + ids[4]).click({ ids: ids }, updatePalette);
}
function updatePalette(e) {
  if (e == undefined)
    e = { data: { ids: ['funcs', 'palettes', 'numedges', 'res', 'submit'] }};
    
  var func = jQuery('#' + e.data.ids[0]).val();
  data[0].func = funcs[func].f;
  data[0].desc = funcs[func].desc;
  jQuery('#desc').html(funcs[func].desc);
  data[0].dims.dx = (data[0].dims.xmax - data[0].dims.xmin) / jQuery('#' + e.data.ids[3]).val();
  data[0].dims.dy = (data[0].dims.ymax - data[0].dims.ymin) / jQuery('#' + e.data.ids[3]).val();
  data[0].palette = jQuery('#' + e.data.ids[1]).val();
  data[0].edges = 1 * jQuery('#' + e.data.ids[2]).val();
  data[0] = DataSeries(data[0]);
//  plot.series[0] = newData;
//  plot.replot();
  plot.series[0].dims = data[0].dims;
  var newData = renderData(data);
  test('mycanvas', data[0]);
  plot.replot();
  return false;
}


var jet_segmentdata = 
{'blue': [[0.0, 0.5, 0.5],
          [0.11, 1, 1],
          [0.34, 1, 1],
          [0.65, 0, 0],
          [1, 0, 0]],
 'green': [[0.0, 0, 0],
           [0.125, 0, 0],
           [0.375, 1, 1],
           [0.64, 1, 1],
           [0.91, 0, 0],
           [1, 0, 0]],
 'red': [[0.0, 0, 0],
         [0.35, 0, 0],
         [0.66, 1, 1],
         [0.89, 1, 1],
         [1, 0.5, 0.5]]};
var accent_segmentdata =
{'blue': [[0.0, 0.49803921580314636, 0.49803921580314636],
          [0.14285714285714285, 0.83137255907058716, 0.83137255907058716],
          [0.2857142857142857, 0.52549022436141968, 0.52549022436141968],
          [0.42857142857142855, 0.60000002384185791, 0.60000002384185791],
          [0.5714285714285714, 0.69019609689712524, 0.69019609689712524],
          [0.7142857142857143, 0.49803921580314636, 0.49803921580314636],
          [0.8571428571428571, 0.090196080505847931, 0.090196080505847931],
          [1.0, 0.40000000596046448, 0.40000000596046448]],
 'green': [[0.0, 0.78823530673980713, 0.78823530673980713],
           [0.14285714285714285, 0.68235296010971069, 0.68235296010971069],
           [0.2857142857142857, 0.75294119119644165, 0.75294119119644165],
           [0.42857142857142855, 1.0, 1.0],
           [0.5714285714285714, 0.42352941632270813, 0.42352941632270813],
           [0.7142857142857143, 0.0078431377187371254, 0.0078431377187371254],
           [0.8571428571428571, 0.35686275362968445, 0.35686275362968445],
           [1.0, 0.40000000596046448, 0.40000000596046448]],
 'red': [[0.0, 0.49803921580314636, 0.49803921580314636],
         [0.14285714285714285, 0.7450980544090271, 0.7450980544090271],
         [0.2857142857142857, 0.99215686321258545, 0.99215686321258545],
         [0.42857142857142855, 1.0, 1.0],
         [0.5714285714285714, 0.21960784494876862, 0.21960784494876862],
         [0.7142857142857143, 0.94117647409439087, 0.94117647409439087],
         [0.8571428571428571, 0.74901962280273438, 0.74901962280273438],
         [1.0, 0.40000000596046448, 0.40000000596046448]]};


// Returns the blend of two colors given a value in a data set
function color_blend(data, value, color_params_type, color_start, color_end) {
  if (!color_params_type) color_params_type = 'hsl';

  blend_alpha = (value - arrayMin(data)) / (arrayMax(data) - arrayMin(data));
  return color_blend_alpha(blend_alpha, color_params_type, color_start, color_end);
}

// Returns the blend of two colors given a blending ratio, and start and end colors
function color_blend_alpha(blend_alpha, color_params_type, color_start, color_end) {
  if (!color_params_type) color_params_type = 'hsl';

  var color_blend = [], color_params = [];
  switch (color_params_type) {
    case 'hsl':
      color_params = [{'param_name': 'Hue',        'suffix': ''},
                      {'param_name': 'Saturation', 'suffix': '%'},
                      {'param_name': 'Luminosity', 'suffix': '%'}];
      break;
    case 'rgb':
      color_params = [{'param_name': 'Red',        'suffix': ''},
                      {'param_name': 'Green',      'suffix': ''},
                      {'param_name': 'Blue',       'suffix': ''}];
      break;
  }
  
  for (var color_param in [0, 1, 2])
    color_blend[color_param] = Math.floor(color_start[color_param] * (1 - blend_alpha) + color_end[color_param] * blend_alpha) + color_params[color_param]['suffix'];
  
  return color_params_type + '(' + color_blend.join(', ') + ')';
}

function color_blend_segments(h, segmentdata) {
  if (h < 0 || h > 1) throw 'Error: h is not in the domain [0, 1]';
  var colors = ['red', 'green', 'blue'];
  var color_blend = [];
  for (var i = 0; i < colors.length; i ++) {
    var colordata = segmentdata[colors[i]];
    var left = searchsorted(colordata, h, 'left', 0);
    var right = Math.min(searchsorted(colordata, h, 'right', 0), colordata.length - 1);
    if (right == left) left -= 1;
    var h_ = (h - colordata[left][0]) / (colordata[right][0] - colordata[left][0]);

    if (!isFinite(h_)) h_ = 0;
    //console.log('#', colordata, ', L:',left, ', R:', right, ', l:', colordata[left][2], ', r:', colordata[right][1], ', h_:', h_);
    color_blend[i] = colordata[left][2] * (1 - h_) + colordata[right][1] * h_;
  }
  return color_blend;
}
