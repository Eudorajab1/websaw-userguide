============
Installation
============

Installing *Websaw* is pretty much a straightforward process as follows:-

* Create a new virtual environment (reccomended for development)
* Activate the venv
* Install websaw using pip

.. important:: 
    Depending on your operating system the installation commands vary slightly.
    example: Windows, you must use backslashes (i.e. ``\``) instead of slashes.
    Please also ensure that you have python >= 3.7 installed along wiht pip and that both are in your os path.


Installation in a production envirnoment is covered later.

So lets get going. The sooner we install Websaw the sooner we can start developing *Awesome* apps!!

.. _quick_start_label:

Quick Start
-----------
   
In order to get started make sure that your os meets the following minimal requirements.

* Pyhton >= 3.7
* pip

For the sake of keeping the instructions generic let us assume that we are woking on a WSL Ubuntu
type development environment.

On Linux OS make sure you have sudo access

For Development purposes we strongly reccomend that you first create a virtual environment in order to
isolate packages and depndancies form your main environment.

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

To deactive the virtual environment simply use the followint command: 
::

    deactivate

This will take you back to your normal python bash prompt

To use Websaw, make sure that your venv is activated and then simply install 
::

    pip install websaw

Once pip has finished installing Websaw and all the required dependancies you should be good to go.

In order to check run the following command 
::

    websaw -h

If you get the following output Websaw has been installed and is ready to use. 
If not please refer to the `Installation`_ section of this manual.
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


Well done .. you are now ready to use your new Websaw installation to create some awesome apps!!
