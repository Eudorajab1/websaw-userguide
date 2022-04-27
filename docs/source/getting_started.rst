
.. _getting_started:

Getting Started
===============
   
Assuming you have successfully installed *Websaw* by following the :ref:`installation_label` procedure you 
should now have the following depending on the installation method you chose.

If you installed using pip:

* latest stable version of websaw and dependancies installed in your venv

If you installed via git:

* latest websaw sourcecode installed in your websaw folder.
* apps directory containing sample apps shipped with *Websaw*
  
If you have installed from source you need to ::

    cd websaw


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

If not please refer to the :ref:`installation_label` section of this manual.

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

Now that we have got our app folder ready lets head over to `Websaw Workshop <https://websaw-workshop.readthedocs.io/en/latest/getting_started.html>`
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
