from fabric.api import cd, run, sudo, prefix, abort
from fabric.contrib.console import confirm
from os import listdir
import os
# Rename Project Name
from django_start.settings import PROJECT_VARIABLES

PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_NAME = PROJECT_VARIABLES['PROJECT_NAME']
os.rename(os.path.join(PATH, 'django_start'), os.path.join(PATH, PRJ_NAME))
DB_PASSWORD = PROJECT_VARIABLES['DB_PASSWORD']
DB_RO_PASSWORD = PROJECT_VARIABLES['DB_RO_PASSWORD']


def install_system_packages():
    try:
        sudo("apt-get update")
    except:
        pass
    try:
        sudo("apt-get upgrade -y")
    except:
        pass
    sudo("apt-get -qy install minicom python-virtualenv git "
         "postgresql libpq-dev python-dev libxslt-dev libldap2-dev "
         "libsasl2-dev freetds-dev g++ unixodbc-dev tdsodbc emacs "
         "apache2 ntp ssmtp pbzip2 supervisor postgresql-contrib "
         "redis-server nginx")


def create_user():
    sudo("groupadd --system %s" % PRJ_NAME)
    sudo("useradd --system --gid %s --shell /bin/bash --home %s/ %s" % (
        PRJ_NAME, PATH, PRJ_NAME))
    sudo("chown %s:%s %s" % (PRJ_NAME, 'users', PATH))


def create_virtual_env():
    run("virtualenv --no-site-packages %s" % (PATH + '/' + '.env'))


def install_pip_packages():
    with cd(PATH):
        with prefix("source %s/.env/bin/activate" % PATH):
            run("pip install -r %s/requirements/latest.txt" % PATH)


def initialize_database():
    sudo("createuser -SDR %s" % PRJ_NAME, user="postgres")
    sudo("""
    psql -c "ALTER ROLE %s WITH PASSWORD '%s'"
    """ % (PRJ_NAME, DB_PASSWORD), user="postgres")
    sudo("createdb -U postgres %s" % PRJ_NAME, user="postgres")
    sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s"' % (
        PRJ_NAME, PRJ_NAME), user="postgres")


def create_read_only_user():
    sudo("createuser -SDR %sro" % PRJ_NAME, user="postgres")
    sudo("""
        psql -c "ALTER ROLE %sro WITH PASSWORD '%s'"
    """ % (PRJ_NAME, DB_RO_PASSWORD), user="postgres")
    sudo("""
        psql -d %s -c "GRANT USAGE ON SCHEMA public TO %sro"
    """ % (PRJ_NAME, PRJ_NAME), user="postgres")
    sudo("""
         psql -d %s -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO %sro"
         """ % (PRJ_NAME, PRJ_NAME), user="postgres")


def update_project():
    with cd(PATH):
        run("git pull origin master")


def install_nginx_config():
    pass

def install_gunicorn_run():
    pass

def install_supervisor_config():
    sudo("cp confs/supervisor.conf /etc/supervisor/conf.d/%s.conf" % PRJ_NAME)



def install_development_copy():
    '''
    Assumes you have cloned your own copy from github to start.
    '''
    global PATH
    install_system_packages()
    create_virtual_env()
    install_pip_packages()
    initialize_database()
    create_read_only_user()
    create_user
    # update_project()
