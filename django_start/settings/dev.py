from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING.update({
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
            }
        },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': True
            }
        }
    })
