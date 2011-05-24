
// Construct module menu from module set definition.
// The module definition looks like
//    [ {group: string, modules: [ string, ...]], ... ]
function emit_module_menu(menu) {
    var i,j, modules;
    emit('<div class="module_selector">');
    emit('<dl>');
    for (i = 0; i < menu.length; i += 1) {
        modules = menu[i].modules;
        emit('<dt>'+menu[i].category+'</dt><dd><ul>');
        for (j = 0; j < modules.length; j += 1) {
            emit('<li>'+modules[i]+'</li>');
        }
        emit('</ul></dd>');
    }
    emit('</dl>');
    emit('</div>\n');
}

function edit_diagram(instrument, diagram) {
    try {
        language = new WireIt.WireingEditor(instrument);
    } catch (ex) {
        alert(ex);
    }
}


