
.. _run_websaw_label:


==============
Running Websaw
==============

For Development purposes the traditional way to run Websaw is from the command line as follows:

::

    python -m websaw run apps

This will attempt to start all applications in the directory apps but you can store your apps in any folder of your
choice. Just make sure to let websaw know the root folder for your applications.

Output in the console should look similar to the below depending on the structure of your root apps directory and the number of applicaitons installed (in this case apps)
::
    
                   __
  ___     ______  / /_  _________ __      __
  | | /| / /> _ \/ __ \/ ___/ __ `/ | /| / />
  | |/ |/ />  __/ /_/ (__  ) /_/ /| |/ |/ />
  |__/|__/>\___/_.___/____/\__,_/ |__/|__/>

    it is just the beginning...

    Websaw: 0.0.6 on Python 3.8.10 (default, Mar 15 2022, 12:22:08)
    [GCC 9.4.0]


    [X] loaded new_app
    [X] loaded pyjsaw
    [X] loaded auth
    [X] loaded app_mixin1
    [X] loaded app_mixin
    [X] loaded db_admin
    [X] already loaded mixins
    [X] loaded todo
    [X] loaded xauth
    [X] loaded simple
    [X] loaded group_session
    Ombott v0.0.13 server starting up (using RocketServer(reloader=False))...
    watching (lazy-mode) python file changes in: apps
    Listening on http://127.0.0.1:8000/
    Hit Ctrl-C to quit.

Starting Websaw form the command line offers you many options to pass in paramters to change the behavbiour of your Websaw instance.

For example::

    python -m websaw run apps -H 0.0.0.0 -P 8010

tells Websaw that we want it to run on IP 0.0.0.0 and Port 8010 and you will see the following:
::

    Ombott v0.0.13 server starting up (using RocketServer(reloader=False))...
    Listening on http://0.0.0.0:8010/
    Hit Ctrl-C to quit.

    watching (lazy-mode) python file changes in: apps

as opposed to the default 127.0.0.1 and port 8000

This is very usefull for development where multiple developers are working on the same application. Each one can run the applicaiton on their own port if necessary and not affect any other instance

.. important::

    By default Websaw will automatically detect any changes to any .py file in the apps structure and restart the server in order to reflect the latest changes.
    You can use the --watch setting in the cli to change this behaviour.

Websaw CLI
----------

In order to see the cli options available to you enter the following from inside your activared venv:
::

    python websaw --help

this will show you the list of all available options that can be used with the Websaw Command Line.

To get help on any of these options simply type::

    websaw <command> --help
    eg: python websaw run --help

This will deisplay the following:-
::

    Usage: python -m websaw run [OPTIONS] APPS_FOLDER

    Run all the applications on apps_folder

    Options:
    -Y, --yes                       No prompt, assume yes to questions
                                    [default: False]
    -H, --host TEXT                 Host name  [default: 127.0.0.1]
    -P, --port INTEGER              Port number  [default: 8000]
    -p, --password_file TEXT        File for the encrypted password  [default:
                                    password.txt]
    -s, --server [default|wsgiref|gunicorn|gevent|waitress|geventWebSocketServer|wsgirefThreadingServer|rocketServer]
                                    server to use  [default: default]
    -w, --number_workers INTEGER    Number of workers  [default: 0]
    -d, --dashboard_mode TEXT       Dashboard mode: demo, readonly, full, none
                                    [default: full]
    --watch [off|sync|lazy]         Watch python changes and reload apps
                                    automatically, modes: off, sync, lazy
                                    [default: lazy]
    --ssl_cert PATH                 SSL certificate file for HTTPS
    --ssl_key PATH                  SSL key file for HTTPS
    -help, -h, --help               Show this message and exit.

The majority of thse options should be self explanetory but there are a few *special* options that we will cover in greater deatail later on.

Right now you should be able to start and stop Websaw from the command line and be in a position to get developing.

