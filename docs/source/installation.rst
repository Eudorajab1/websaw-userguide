
.. _installation_label:

============
Installation
============

*Websaw* can be installed in a number of ways as follows:-

* Installing from pip using venv (reccommended for development) 
* Installing from git repo locally (reccomended for contributors)
* Installing for production
  
We will cover the first two options below and look at the different production installations in a later section.

In both cases above you will need to do the following:

* Create a new virtual environment (reccomended for development)
* Activate the venv
* Install websaw using either pip (reccomended) or downloading directly from the git repo.

.. important:: 
    Depending on your operating system the installation commands vary slightly.
    example: Windows, you must use backslashes (i.e. ``\``) instead of slashes.
    Please also ensure that you have python >= 3.7 installed along wiht pip and that both are in your os path.

In order to get started make sure that your os meets the following minimal requirements.

* Pyhton >= 3.7
* pip

For the sake of keeping the instructions generic let us assume that we are woking on a WSL Ubuntu
type development environment.

On Linux OS make sure you have sudo access

So lets get going. The sooner we install Websaw the sooner we can start developing *Awesome* apps!!

Installation with pip (preferred)
---------------------------------

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

To install *Websaw* using pip simply run the following 
::

    pip install websaw

Once pip has finished installing websaw and all depencies you will have the latest stable version of *Websaw* and all dependancies installed in your venv and are ready to go.

Installing from source
----------------------

In order to install source from the git repo you will need to have git installed and configured on your machine along with a vailid github account setup.


Same steps as above for creating and activating your venv.

Form inside your activated venv run the following
::

    git clone <path to repo>
  
By default git will create a websaw folder in your dev enviroment.

So lets head into the websaw directory and run 
::

    cd websaw
    pip install -e .

This will give us the latest version of *Websaw* should we need to create any PR's to the Websaw git repo.

*We are now good to go* so lets get started buy heading over to the :ref:`getting_started` section
    