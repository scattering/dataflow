from apps.common.autoadmin import register_all_models
from . import models

options = {
    # 'Model': { 'option': value, ... },
    'Facility': {'readonly': True},
    'Instrument': {'readonly': True},
}

register_all_models(models, options)

