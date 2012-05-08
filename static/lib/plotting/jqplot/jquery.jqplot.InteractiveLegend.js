(function($) {
    // class $.jqplot.InteractiveLegendRenderer
    // The default legend renderer for jqPlot.
    $.jqplot.InteractiveLegendRenderer = function(){
        $.jqplot.TableLegendRenderer.call(this);
    };
    
    // $.jqplot.eventListenerHooks.push(['jqplotClick', handleClick]);
    
    $.jqplot.InteractiveLegendRenderer.prototype = new $.jqplot.TableLegendRenderer();
    $.jqplot.InteractiveLegendRenderer.prototype.constructor = $.jqplot.InteractiveLegendRenderer;
    
    $.jqplot.InteractiveLegendRenderer.prototype.init = function(options) {
        $.extend(true, this, options);
        //$.jqplot.eventListenerHooks.push(['jqplotClick', handleClick]);
    };
        
    $.jqplot.InteractiveLegendRenderer.prototype.addrow = function (label, color, pad, reverse, series_num, series_show) {
        var rs = (pad) ? this.rowSpacing : '0';
        var tr,
        	elem;
        if (reverse){
            tr = $('<tr class="jqplot-table-legend"></tr>').prependTo(this._elem);
        }
        else{
            tr = $('<tr class="jqplot-table-legend"></tr>').appendTo(this._elem);
        }
        var color = series_show ? color : "transparent";

            $('<td class="jqplot-table-legend" style="text-align:center;padding-top:'+rs+';">'+
            '<div><div class="jqplot-table-legend-swatch" style="background-color:'+color+
            ';border-color:'+color+';width:10px;height:10px;"></div>'+
            '</div></td>').appendTo(tr);
        
        //if (this.showLabels) {
            elem = $('<td class="jqplot-table-legend-label" style="padding-top:'+rs+';" series_num='+series_num+'></td>');
            elem.appendTo(tr);
            if (this.escapeHtml) {
                elem.text(label);
            }
            else {
                elem.html(label);
            }
        //}
        elem.click({legend: this}, handleClick);
        tr = null;
        elem = null;
    };
    // 'width:10px;height:10px;
    // called with scope of legend
    $.jqplot.InteractiveLegendRenderer.prototype.draw = function() {
        var legend = this;
        if (this.show) {
            var series = this._series;
            // make a table.  one line label per row.
            var ss = 'position:absolute;';
            ss += (this.background) ? 'background:'+this.background+';' : '';
            ss += (this.border) ? 'border:'+this.border+';' : '';
            ss += (this.fontSize) ? 'font-size:'+this.fontSize+';' : '';
            ss += (this.fontFamily) ? 'font-family:'+this.fontFamily+';' : '';
            ss += (this.textColor) ? 'color:'+this.textColor+';' : '';
            ss += (this.marginTop != null) ? 'margin-top:'+this.marginTop+';' : '';
            ss += (this.marginBottom != null) ? 'margin-bottom:'+this.marginBottom+';' : '';
            ss += (this.marginLeft != null) ? 'margin-left:'+this.marginLeft+';' : '';
            ss += (this.marginRight != null) ? 'margin-right:'+this.marginRight+';' : '';
            this._elem = $('<table class="jqplot-table-legend" style="'+ss+'"></table>');
        
            var pad = false, 
                reverse = false,
				s;
            for (var i = 0; i< series.length; i++) {
                s = series[i];
                if (s._stack || s.renderer.constructor == $.jqplot.BezierCurveRenderer){
                    reverse = true;
                }
                //if (s.show && s.showLabel) {
                    var lt = this.labels[i] || s.label.toString();
                    if (lt) {
                        var color = s.color;
                        if (reverse && i < series.length - 1){
                            pad = true;
                        }
                        else if (reverse && i == series.length - 1){
                            pad = false;
                        }
                        this.renderer.addrow.call(this, lt, color, pad, reverse, i, s.show);
                        pad = true;
                    }
                    // let plugins add more rows to legend.  Used by trend line plugin.
                    for (var j=0; j<$.jqplot.addLegendRowHooks.length; j++) {
                        var item = $.jqplot.addLegendRowHooks[j].call(this, s);
                        if (item) {
                            this.renderer.addrow.call(this, item.label, item.color, pad);
                            pad = true;
                        } 
                    }
                    lt = null;
                //}
            }
        }
        return this._elem;
    };
    
    function handleClick(ev) {
        if (debug) {console.log(ev);}
        if (ev.data && ev.data.legend && ev.data.legend.handleClick) {
            ev.data.legend.handleClick(ev);
        } 
    } 
    
})(jQuery);

