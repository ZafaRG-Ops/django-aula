######################################
Django-Aula: Anotacions d'instal·lació
######################################

Aquest document descriu les passes per a poder realitzar una instal·lació
de l'aplicació djau amb una màquina virtual de Vagrant

L'objectiu és aconseguir modificar-ho fins que sigui totalment
automatitzable.

VirtualBox
==========

::

    $ echo "deb http://download.virtualbox.org/virtualbox/debian stretch contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list
    $ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
    $ wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
    $ sudo apt-get update
    $ sudo apt-get install virtualbox-6.0

Vagrant
=======

::

    $ wget -c https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
    $ sudo dpkg -i vagrant_2.2.6_x86_64.deb
    $ vagrant --version
    $ vagrant box add ubuntu/bionic64
    $ vagrant init ubuntu/bionic64

    # Editar a Vagrantfile una interficie de xarxa privada
    # de manera que pugui accedir des de 192.168.33.10
    # És bàsicament descomentar una línia
    $ grep private_network Vagrantfile
      config.vm.network "private_network", ip: "192.168.33.10"


    $ vagrant up
    $ vagrant ssh
    … aquí fes el que et calgui a la màgina virtual que acabes de crear
    $ vagrant halt


Requeriments del sistema
========================

Les següents instruccions són a la MV

::

    $ sudo apt update
    $ sudo apt upgrade
    $ sudo apt install libxml2-dev libxslt1-dev git lib32z1-dev \
                       python3-dev python3-pip python3-psycopg2
    $ sudo -H python3 -m pip install pipenv

PostgreSQL
==========

::

    $ sudo apt install apache2 libapache2-mod-wsgi-py3 postgresql postgresql-server-dev-10
    $ sudo su postgres
    $ psql
    postgres=# CREATE DATABASE djau2019;
    postgres=# CREATE USER djau2019 WITH PASSWORD 'passwordsuperxungo';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE djau2019 TO djau2019;
    postgres=# \q
    $ exit


Obtenció de Django-aula
=======================

::

    $ cd /opt
    $ sudo git clone «path-to-git-repository-with-django-aula.git» djau2019
    #           https://github.com/ZafaRG-Ops/django-aula.git
    # El disseny original recomana una instal·lació per cada any
    $ sudo chown -R vagrant.vagrant djau2019
    $ cd djau2019
    $ pipenv update
    $ pipenv install wheel
    $ ln -s `pipenv --venv` venv
    # $ sudo pipenv shell

Configuració de Django-aula
===========================

El fitxer de configuració

Considera més documentació sobre la parametrització de djau a: https://github.com/ctrl-alt-d/django-aula/blob/master/docs/manuals/parametritzacions.txt

settings_local.py
-----------------

::

    $ cd /opt/djau2019/aula
    # edita settings_local.py segons

        # This Python file uses the following encoding: utf-8
        # Django settings for aula project.

        from settings_dir.common import *

        NOM_CENTRE = 'IES Joan d\'Àustria'
        LOCALITAT = u"Barcelona"
        URL_DJANGO_AULA = r'https://insjoandaustria.xtec.cat/dawm15'

        # Hosts amb accés a l'aplicació (per defecte '*' permet tothom amb accés a la màquina
        # fer servir l'aplicació)
        # Es poden col·locar adreces en format CIDR o dominis (s'accepten wildcards)
        ALLOWED_HOSTS =  [ '*', ]

        ACCES_RESTRINGIT_A_GRUPS = None # ó be = ['direcció','administradors']  mentre duran les proves

        #En cas de tenir un arbre de predicció cal posar-lo aquí:
        # from lxml import etree
        # PREDICTION_TREE=etree.parse( r'path_fins_el_model' )
        PREDICTION_TREE = None
        location = lambda x: os.path.join(PROJECT_DIR, x)
        BI_DIR = '/opt/djau2019/aula/apps/BI/PMML'
        #__PREDICTION_TREE_TMP = os.path.join( BI_DIR, 'previsioPresencia.pmml' )
        #from lxml import etree
        #PREDICTION_TREE = etree.parse( __PREDICTION_TREE_TMP )

        INSTALLED_APPS  = [] + INSTALLED_APPS


        STATIC_URL = '{domain}/site-css/'.format( domain=URL_DJANGO_AULA )
        STATIC_ROOT = '/home/djau/webapps/djaustatic/'

        EMAIL_SUBJECT_PREFIX = '[DJANGO AULA] '

        DEBUG = False

        # Dades de l'administrador
        ADMINS = (
            ('Moisès Gómez', 'moises.gomez@iesjoandaustria.org'),
        )

        # Configuració del correu
        EMAIL_HOST='smtp.gmail.com'
        EMAIL_HOST_USER='djaujda@gmail.com'
        EMAIL_HOST_PASSWORD='passwordsupersecret'
        DEFAULT_FROM_EMAIL = "IES Joan d'Àustria <djaujda@gmail.com>"
        EMAIL_PORT=587
        EMAIL_USE_TLS=True
        SERVER_EMAIL='djaujda@gmail.com'
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_SUBJECT_PREFIX = "[Comunicació IES Joan d'Àustria] "


        #Ruta donde almacenara los assets de la aplicacion
        STATICFILES_DIRS =  STATICFILES_DIRS
        STATIC_ROOT= os.path.join(PROJECT_DIR,'static/')

        #Comprime los assets estaticos de la app False por defecto
        COMPRESS_ENABLED = False

        #Passphrase que usara la app para cifrar las credenciales
        SECRET_KEY = 'changeit'
        CUSTOM_RESERVES_API_KEY = 'sxxxxxxm'

        #Componente que utilizara  Django para serializar los objetos
        SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

        #Configuracion de la Base de datos
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2', #django.db.backends.mysql *para mysql
                'NAME': 'djau2019',
                'USER': 'djau2019',
                'PASSWORD': "passwordsuperxungo",
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        PRIVATE_STORAGE_ROOT ='/dades/fitxers_privats_djAu/'

fixtures
--------

    $ cd /opt/djau2019
    $ pipenv shell
    $ python manage.py migrate
    $ bash scripts/fixtures.sh

    # Creem un administrador
    $ python manage.py createsuperuser
    Nom d'usuari (leave blank to use 'vagrant'): admin
    Adreça de correu electrònic: djaujda@gmail.com
    Password: passwordsupersecret
    Password passwordsupersecret
    Superuser created successfully.

    # Afegim l'administrador al grup de direcció, professors i
    # professional, de manera que pugui iniciar sessió

    $ python manage.py shell
    >>> from django.contrib.auth.models import User, Group
    >>> g1 = Group.objects.get(name='direcció')
    >>> g2 = Group.objects.get(name='professors')
    >>> g3 = Group.objects.get(name='professional')
    >>> a = User.objects.get(username='admin')
    >>> a.groups.set([g1, g2, g3])
    >>> a.save()
    >>> quit()

    # agrupem el contingut static en una sola carpeta
    $ python manage.py collectstatic

Configuració del Apache
=======================

::

    $ sudo locale-gen ca_ES,utf8
    $ sudo a2enmod ssl      # per quan fem servir ssl

    $ sudo vi /etc/apache2/sites-available/djau.conf

    <VirtualHost *:80>
            ServerAdmin djaujda@gmail.com
            ServerName insjoandaustria.xtec.cat

            WSGIDaemonProcess djau python-home=/opt/djau2019/venv python-path=/opt/djau2019 \
                locale="ca_ES.utf8"
            WSGIProcessGroup djau
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptAlias / /opt/djau2019/aula/wsgi.py

            #Alias para contenido estatico de la app

            Alias /site-css/admin /opt/djau2019/static/admin/
            Alias /site-css /opt/djau2019/static/

            ErrorLog /var/log/apache2/djau_error.log

            #Dando acceso a apache a los directorios de la app
            <Directory /opt/djau2019/aula>
                    <Files wsgi.py>
                            Require all granted
                    </Files>
            </Directory>

            <Directory /opt/djau2019/static/>
                    Require all granted
            </Directory>


            <Directory /opt/djau2019/static/admin/>
                    Require all granted
            </Directory>

            LogLevel info

            CustomLog /var/log/apache2/djau_access.log combined

            BrowserMatch ".*MSIE.*" \
                    nokeepalive ssl-unclean-shutdown \
                    downgrade-1.0 force-response-1.0

    </VirtualHost>


    # A continuació la versió ssl (de moment no provada!)
    $ sudo vi /etc/apache2/sites-available/djau_ssl.conf


    # Cal indicar que funcioni amb SSL (TLS) a /opt/djau2019/aula/settings_local.py
    # Cal activar el mòdul ssl: a2enmod ssl

    <VirtualHost *:443>

            ServerAdmin djaujda@gmail.com
            ServerName insjoandaustria.xtec.cat

            WSGIDaemonProcess djau python-home=/opt/djau2019/venv python-path=/opt/djau2019 \
                locale="ca_ES.utf8"
            WSGIProcessGroup djau
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptAlias / /opt/djau2019/aula/wsgi.py

            # Alies pel contingut static

            Alias /site-css/admin /opt/djau2019/aula/static/admin/
            Alias /site-css /opt/djau2019/aula/static/

            ErrorLog /var/log/apache2/djau_ssl_error.log

            #Dando acceso a apache a los directorios de la app
            <Directory /opt/djau2019/aula>
                    <Files wsgi.py>
                            Require all granted
                    </Files>
            </Directory>

            <Directory /opt/djau2019/aula/static/>
                    Require all granted
            </Directory>


            <Directory /opt/djau2019/aula/static/admin/>
                    Require all granted
            </Directory>

            #SSL Config#########################

            # Generar SelfSignedCertificate
            # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/badia-selfsigned.key -out /etc/ssl/certs/badia-selfsigned.crt

            SSLEngine on
            SSLCertificateFile /etc/ssl/certs/badia-selfsigned.crt
            SSLCertificateKeyFile /etc/ssl/private/badia-selfsigned.key
            LogLevel warn

            #SSL Config#######################

            LogLevel info

            CustomLog /var/log/apache2/djau_ssl_access.log combined

            BrowserMatch ".*MSIE.*" \
                    nokeepalive ssl-unclean-shutdown \
                    downgrade-1.0 force-response-1.0

    </VirtualHost>

    # De moment farem servir només la versió del port 80
    $ sudo chown -R www-data.www-data /opt/djau2019

    # Donat que estem fent servir pipenv i el venv ha quedat guardat
    # al /home/vagrant/.local, també caldrà afegir permisos per a
    # accedir-hi a www-data. De moment, he afegit www-data al grup vagrant
    # Però caldrà mirar si és una solució segura per producció
    $ sudo adduser www-data vagrant

    # Cal editar el fitxer /opt/djau2019/aula/settings_dir/common.py i
    # afegir '*' a allowed-hosts
    $ grep ALLOWED_HOSTS /opt/djau2019/aula/settings_dir/common.py
    ALLOWED_HOSTS = ['*']

    # Atenció: caldrà estudiar aquest fitxer doncs conté elements de
    # configuració com ara el nom de l'administrador.

    $ sudo a2dissite 000-default.conf
    $ sudo a2ensite djau.conf
    # sudo a2ensite djau_ssl.conf
    $ sudo systemctl reload apache2


TODO List
=========

* estudiar el fitxer /opt/djau2019/aula/settings_dir/common.py

  Conté elements de configuració com ara el nom de l'administrador.

* Estudiar com automatitzar aquestes instruccions de manera que puguin ser
  executades sense assistència.
