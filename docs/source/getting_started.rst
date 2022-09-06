
.. _getting_started:

Getting Started
===============

**WebSaw** can be used completely standalone to provide a fully funcitonal, feature rich, web frameowork.
 
For more complex development requirements or to develop in a more pythonic way we reccomend you take a look at the 
following complimentory libraries/packages which have been developed to integrate seamlessly with **Websaw**.

.. important::
    All the below work completely independantly of **WebSaw** and can be used standalone in their own right. There is no dependancy on **WebSaw** and no need
    to use them with **WebSaw** but they definately do add value and improve on the whole developemtn experience.

* For rapid **SPA** development **Pyjsaw** is an absolute must. This fully featured trasnpiler generates pure .JS apps using pythonic code.
* **Voodoodal** wrapper for the industry standard **pydal** data access layer library providng a pythonic methods for table definition and DB access.

**WebSaw** ships as standard with the **YATL** template renderer but we strongly reccomend installing **UPYTL** and using it insted of standard html templates
as this allows us to create re-usable components without having to write a single line of HTML code as we will see later.

**UPYTL** ships with a set of *standard* components which include all the html types as well as many of the industry standard database field types in order
to get you up and running in a matter of minutes.

**Advanced** or tailored components are available to enterprise clients for a minimal fee.

Once again there is no need to install any of the above in order to use **WebSaw** but we strongly reccomend taking a look at the above.

.. _installation_label:

Installation
------------
*WebSaw* can be installed on most operating systems including Windows, Linux, MacOS and is totally OS agnostic.


Requirements
------------

* Pyhton >= 3.8
* pip
* git

.. important:: 
    Depending on your operating system the installation commands vary slightly. For example: Windows, you must use backslashes (i.e. ``\``) 
    instead of slashes. Please also ensure that you have python >= 3.8 installed along with pip and git and that are are in your os path. 

* Installing from pip 
* Installing from git repo locally (reccomended)
* Installing for production
* Installing user Docker
  
Installing using PyPi
---------------------

.. note::
    Whilst not necessary, we strongly reccomend that you create a virtual environemnt on your OS before installing **WebSaw**. 
    Relevant instructions on createint a virtual envirnonment for your OS are beyond the scope of this document.

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

This is python’s way of telling us that we are now in the virtual environment and we can start installing Websaw.

To deactive the virtual environment at any time simply use the following command: 
::

    deactivate

This will take you back to your normal python bash prompt. For now lets keep the venv activated.

::

    pip install websaw

Thats it you are good to go

Installing from source locally
------------------------------

if you want to install into your local environment please do the following:

:: 

    git clone https://github.com/valq7711/websaw.git
    cd websaw
    pip install -e .

Installing from source globally
-------------------------------

:: 

    git clone https://github.com/valq7711/websaw.git
    cd websaw


Docker Compose
--------------

:: 

    git clone https://github.com/valq7711/websaw.git
    cd websaw
    docker-compose up

The Docker container automatically pulls **PyjSaw**, **UPYTL** and **voodoodal** which makes them all available.


*We are now good to go* so lets get started buy heading over to the :ref:`getting_started` section
    


Assuming you have successfully installed *Websaw* should now have the following depending on the installation method you chose.

If you installed using pip:

* latest stable version of websaw and dependancies installed in your venv

If you installed via git:

* latest websaw sourcecode installed in your websaw folder.
* apps directory containing sample apps shipped with *Websaw*
  
If you have installed from source you need to ::

    cd websaw

if you haver installed using a Docker container you have everything you need inside your dokcer container called websaw.

Irrespective of installation method lets verify that *Websaw* has installed correctly as follows: 
::

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

If not please refer to the Installation section of this manual.

So lets take a look at creating a new app and let us call that app hello_world.

For git installations the first step is not necessary as the apps folder and a few example apps are already installed so you can skip this first step.

So the first thing we can do is use the CLI to help us. 

The ClI has many commands and options which will be covered in its own section later on so for now lets run the following:
::

    python -m websaw setup apps

This will create the <apps> folder for us in our root folder. In this case we have chosen to name it apps but it could just as well be any valid folder.

Now lets create our hello world app as a new app by running the following:-
::

    python -m websaw new_app <path/to/scaffolding/app>

The scaffolding app zipfile shoudl be in your root directory by default

For git installations the easiest thing to do is just copy the apps/simple folder or rename it to heelo_world

In all cases it is just as easy to create both the apps folder and the hello_world app folder manually
::

    mkdir apps ## if does not exist
    cd apps
    touch . __init__py
    mkdir hello_world
    cd hello_world
    touch . __init__.py

or by using your favourite IDE such as vscode.

Now that we have got our app folder ready lets head over to `Websaw Workshop <https://websaw-workshop.readthedocs.io/en/latest/getting_started.html>`_
to put everything to use.

Once you have completed the first workshop you will have seen how the three main layers of 
*Websaw* in action.
    
    * **Fixture**
    * **Context**
    * **Application**

You will also note that so far we have not mentioned things like **request**, **response** and **sessions** that make up any 
HTTP framework.

This does not mean that they are not there .. far from it. 

We will cover these in the :ref:`context` section of the user guide but for now lets take a deeper look 
at the  **fixture** layer by heading over to the :ref:`fixtures` seciton.
