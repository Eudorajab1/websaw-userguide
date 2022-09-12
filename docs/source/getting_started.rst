
.. _getting_started:

Getting Started
===============

.. _requirements_label:

Requirements
------------

    * Python >= 3.8
    * git
    * pip
    * venv or virtualenv **reccomended**
  
.. _installation_label:

Installation
------------

**WebSaw** can be installed on most operating systems including Windows, Linux, MacOS and is totally OS agnostic.

**WebSaw** ships as standard with the **UPYTL**, **PyJSaw** and **Voodoodal** all of which will be covered in greater depth in the appropriate seciton of this user guide.

.. note::
    Whilst not necessary, we strongly reccomend that you create a virtual environemnt on your OS before installing **WebSaw**. 
    Relevant instructions on creating a virtual envirnonment for your OS are beyond the scope of this document.

So lets start by taking a simple use case:

For the sake of keeping the instructions generic let us assume that we are woking on a WSL Ubuntu
type development environment.

Creating a Virtual Environment
------------------------------

To do this you need to open a new bash / shell / cmd window and enter the following:-
::

    python3 -m venv <direcory_name>
    cd <directory_name>
    source ./bin/activate

This above will create a python3 virtual environment and activiate it.

If all is good your prompt will change to the name of the vitual environment you have activated: 
::

    (directory_name)$

To deactive the virtual environment at any time simply use the following command: 
::

    deactivate

This will take you back to your normal python bash prompt. For now lets keep the venv activated.

.. important:: 
    Depending on your operating system the installation commands vary slightly. For example: Windows, you must use backslashes (i.e. ``\``) 
    instead of slashes. Please also ensure that your operating system complies with the :ref:`requirements_label` 


The main ways to install **Websaw** are as follows:

    * Installing from PyPi / pip 
    * Installing from git repo locally (reccomended)
    * Installing for production
    * Installing using Docker *# make sure you have the latest docker and docker-compose installed on your OS*
  
Installing using PyPi
---------------------
In your newly created virtual enviroment enter the following:
::

    pip install websaw
    python -m websaw setup apps # this will create a folder called aspps and populate it with the sample apps that ship with **WebSaw**
    python -m websaw set_password # will prompt you for and admin password and confirmation

Thats it you are good to go

Installing from source locally
------------------------------
if you want to install into your local environment please do the following:
:: 

    git clone https://github.com/valq7711/websaw.git
    cd websaw # note apps directory is populated with sample apps   
    pip install -e . #installs websaw to your local environment.
    python -m websaw set_password # will prompt you for and admin password and confirmation

Installing from source globally
-------------------------------
:: 

    git clone https://github.com/valq7711/websaw.git
    cd websaw
    python -m websaw set_password # will prompt you for and admin password and confirmation

Docker Compose
--------------
:: 

    git clone https://github.com/valq7711/websaw.git
    cd websaw
    docker-compose up

Whatever your preferred method for installation you should by now now have the latest stable version of **WebSaw** and all dependancies installed in your venv
or docker container

If you have installed from source you need to
::

    cd websaw

if you have installed using the Docker option you already have everything you need inside your dokcer container called websaw 
and **WebSaw** will automatically start when the container is intialised and your **WebSaw** apps wil be 
be running and listening on port 8000

In order to test it head on over to your browser and go to  http://localhost:8000/simple or alternatively click the link.

If you see a page then all is working correctly.

For all other installtion methods lets verify that *Websaw* has installed correctly as follows: 
::
    # from the directory where you apps folder is 
    
    pythn -m websaw -h

If you get the following output Websaw has been installed and is ready to use. 
::

    Usage: python -m websaw [OPTIONS] COMMAND [ARGS]...

    WEBSAW - a web framework for rapid development with pleasure

    Type "websaw COMMAND -h" for available options on commands

    Options:
        -help, -h, --help  Show this message and exit.

    Commands:
        call          Call a function inside apps_folder
        new_app       Create a new app copying the scaffolding one
        run           Run all the applications on apps_folder
        set_password  Set administrator's password for the Dashboard
        setup         Setup new apps folder or reinstall it
        shell         Open a python shell with apps_folder's parent added to...
        version       Show versions and exit

If not please refer to the ::ref:`installation_lable` section.

The easiest way to do this is just copy the apps/scaffold folder or rename it to hello_world

In all cases it is just as easy to create both the apps folder and the hello_world app folder manually
::

    mkdir apps ## if does not exist
    cd apps
    touch . __init__py
    mkdir hello_world
    cd hello_world
    touch . __init__.py

or by using your favourite IDE such as pyjsaw or vscode.

Now that we have got our app folder it is time to head over to the appropriate secion depending on the **Type** of 
application your are looking to develop. 

For *Client Side* or **SPA** application development please refer to :ref:`client_side` alternatively take a look at the :ref:`server_side` section of the user guide.
to get up and running with the application type of your choice.

For a more detailed look at **WebSaw** application development there is a comprehensive set of **Tutorials**
designed to provide you with a comprehensive set of building blocks to get you up to speed using real life hands-on 
practical examples. To learn more please head on over to the `Websaw Workshop <https://websaw-workshop.readthedocs.io/en/latest/getting_started.html>`_
