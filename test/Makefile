SOURCE=../../js_src
T=www/js
CANVAS=$(SOURCE)/excanvas_r3
YUI=$(SOURCE)/yui_2.8.2/
WIREIT=$(SOURCE)/WireIt-0.5.0

all: $Texcanvas-min.js $Twireit-editor-min.js \
     $Tyui-yahoo-min.js $Tyui-event-min.js $Tyui-connection-min.js \
     $Tyui-json-min.js $Tyui-utilities-min.js

$Texcanvas-min.js: $(CANVAS)/excanvas.compiled.js
	cp $< $@
$Twireit-editor-min.js: $(WIREIT)/wiring-editor-min.js
	cp $< $@
$Tyui-yahoo-min.js: $(YUI)/yahoo/yahoo-min.js
	cp $< $@
$Tyui-event-min.js: $(YUI)/event/event-min.js
	cp $< $@
$Tyui-connection-min.js: $(YUI)/connection/connection-min.js
	cp $< $@
$Tyui-json-min.js: $(YUI)/json/json-min.js
	cp $< $@
$Tyui-utilities-min.js: $(YUI)/utilities/utilities.js
	cp $< $@



clean:
	-rm *.js ~*
