import inspect

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models.base import ModelBase

ADMIN_OPTIONS = {'actions', 'actions_on_top', 'actions_on_bottom',
                 'actions_selction_counter', 'date_hierarchy', 'exclude',
                 'fields', 'fieldsets', 'filter_horizontal', 'filter_vertical',
                 'form', 'formfield_overrides', 'inlines', 'list_display',
                 'list_display_links', 'list_editable', 'list_filter',
                 'list_max_show_all', 'list_per_page', 'list_select_related',
                 'ordering', 'paginator', 'prepopulated_fields',
                 'preserve_filters', 'radio_fields', 'raw_id_fields',
                 'readonly_fields', 'save_as', 'save_on_top', 'search_fields',
                 'view_on_site', 'add_form_template', 'change_form_template',
                 'change_list_template', 'delete_confirmation_template',
                 'delete_selected_confirmation_template',
                 'object_history_template', 'save_model', 'delete_model',
                 'save_formset', 'get_ordering', 'get_search_results',
                 'save_related', 'get_readonly_fields',
                 'get_prepopulated_fields', 'get_list_display',
                 'get_list_display_links', 'get_fields', 'get_fieldsets',
                 'get_list_filter', 'get_search_fields', 'get_inline_instances',
                 'get_urls', 'get_form', 'get_formsets_with_inlines',
                 'formfield_for_foreignkey', 'formfield_for_manytomany',
                 'formfield_for_choice_field', 'get_changelist',
                 'get_changelist_form', 'get_changelist_formset',
                 'has_add_permission', 'has_change_permission',
                 'has_delete_permission', 'get_queryset', 'message_user',
                 'get_paginator', 'response_add', 'response_change',
                 'response_delete', 'add_view', 'change_view',
                 'changelist_view', 'delete_view', 'history_view', 'Media',
                 'form', 'inlines'}
def get_model_fields(model):
    return model._meta.fields

def register_all_models(module, options={}, defaults={}):
    """
    Register all models defined within a module.

    *options* is a dictionary of model names and any special options that
    should be given to the admin class for that model.  If options is None,
    then no admin model will be created for that model.  If list_display is
    not given for a model, then every model field is assumed to be a
    list display field.

    *defaults* is a dictionary of defaults for all models

    Special options
    ---------------

    "-list_display": []

        display all but the given fields in the table view

    "-list_editable": []

        don't edit the given fields in the the table view

    "readonly": True|False

        if table is read_only, can't add, delete or edit rows.

    """
    for model_name,model in inspect.getmembers(module):
        #print k, type(v)
        if isinstance(model, ModelBase) and model.__module__ == module.__name__:
            # handle special options:
            #    None => no edit
            #    ModelAdmin class => register that class
            model_detail = options.get(model_name,{})
            if model_detail is None: continue
            if isinstance(model_detail, admin.ModelAdmin):
                admin.site.register(model, admin_class=model_detail)
                continue

            # Assume the model detail is an options dictionary
            model_options = defaults.copy()
            model_options.update(model_detail)
            fields = [f.name for f in get_model_fields(model)]

            if 'readonly' in model_options:
                if model_options['readonly']:
                    model_options['has_add_permission'] = never_do
                    model_options['has_delete_permission'] = never_do
                    model_options['readonly_fields'] = fields
                    model_options['list_editable'] = []
                    model_options['actions'] = None
                del model_options['readonly']


            # Build list display option either by listing excluded fields or
            # included fields.  If not specified, include everything.
            if '-list_display' in model_options:
                model_options['list_display'] = tuple(f for f in fields
                                                  if f not in model_options['-list_display'])
                del model_options['-list_display']
            if 'list_display' not in model_options:
                model_options['list_display'] = tuple(f for f in fields)

            # Build list display option either by listing excluded fields or
            # included fields.  If not specified, include all display fields.
            # Note: first field is key field and is not editable in the list.
            if '-list_editable' in model_options:
                model_options['list_editable'] = tuple(f for f in model_options['list_display']
                                                   if f not in model_options['-list_editable'])
                del model_options['-list_editable']
            if 'list_editable' not in model_options:
                model_options['list_editable'] = model_options['list_display'][1:]

            for opt_name in model_options.keys():
                if opt_name not in ADMIN_OPTIONS and not opt_name.startswith('clean_'):
                    raise ValueError('invalid admin option %r for model %r'%(opt_name,model_name))
            #print Admin.list_display
            try:
                admin.site.register(model, **model_options)
                #print "registered",k,model_options
            except AlreadyRegistered:
                pass
                #print "already registered",k

def always_do(*args, **kw): return True
def never_do(*args, **kw): return False

