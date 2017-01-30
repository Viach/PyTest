MANAGE=django-admin.py

#test:
#	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=pytest.settings $(MANAGE) test hello

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=pytest.settings $(MANAGE) runserver

syncdb:
PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=pytest.settings $(MANAGE) syncdb --noinput
