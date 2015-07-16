ENV ?= development                                                                       
PRJ_NAME ?= django_start
DJANGO_SETTINGS_MODULE ?= $(PRJ_NAME).settings.dev
DJANGO_WSGI_MODULE ?= $(PRJ_NAME).wsgi

dependencies:                                                                  
	pip install -r requirements/${ENV}.txt                             

develop: dependencies                                                          
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) python manage.py syncdb   

devserver:                                                                     
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) python manage.py runserver 0.0.0.0:8000

prodserver:
	NAME=$(PRJ_NAME)
	DJANGODIR=
	SOCKFILE=
	USER=$(PRJ_NAME)
	GROUP=$(PRJ_NAME)
	NUM_WORKERS=3
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE)
	DJANGO_WSGI_MODULE=$(DJANGO_WSGI_MODULE)
	
