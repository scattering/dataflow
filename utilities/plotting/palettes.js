var _fs = function(ks) {
  return function(i) { return $.map($.map(ks, _f), function(f) { return f(i); }); };
};
var _f = function(k) {
  return function(i) { return k * i; };
};
var _mapify = function(rgbfunc) {
  return function(n) {
    var map = [];
    for (var i = 0; i < 1; i += 1 / n)
      map.push(scale_min_floor(rgbfunc(i), 255));
    return map;
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
  myjet: _h2rgb,
  jet: function(h) { return color_blend_segments(h, jet_segmentdata); },
});




var jet_segmentdata = 
{'blue': [[0.0, 0.5, 0.5],
          [0.11, 1, 1],
          [0.34000000000000002, 1, 1],
          [0.65000000000000002, 0, 0],
          [1, 0, 0]],
 'green': [[0.0, 0, 0],
           [0.125, 0, 0],
           [0.375, 1, 1],
           [0.64000000000000001, 1, 1],
           [0.91000000000000003, 0, 0],
           [1, 0, 0]],
 'red': [[0.0, 0, 0],
         [0.34999999999999998, 0, 0],
         [0.66000000000000003, 1, 1],
         [0.89000000000000001, 1, 1],
         [1, 0.5, 0.5]]};


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
  for (i in colors) {
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