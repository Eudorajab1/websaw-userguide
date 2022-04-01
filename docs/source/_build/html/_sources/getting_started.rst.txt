
.. _getting_started:

Getting Started
===============
   
Assuming you have successfully installed *Websaw* by following the :ref:`installation_label` procudure you should now have the following depending on what installation method you chose.

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

This also leads us into the next section where we will look at developing the ubiquitous Hello World app which will provice you with some building blocks for deleoping your aswesam *Websaw* apps.

Before we do .. lets initialise out apps forlder and create a new app.

For git installations the first step is not necessary as the apps folder and a few example apps are already installed so you can skip this first step.

So the first thing we need to do is use the CLI to help us. 

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

or by using your favourite dev ide such as vscode.

As I genrally use vscode simply type code . in the root directory brings up a new instande of vscode


Our First Application
---------------------

As per tradition we are going to create a simple Hello World app to understnad the basics of the *Websaw* framewok after which 
we will get into a lot more depth and detail regarding the tools and techniques being used.

For those of you who want to dive right into a slightly more complex application there is a dedicated 
`Websaw Examples and Tutorials <https://eudorajab1.github.io/>`_ that will walk you through some of the more complex examples.

Either way it you are new to *Websaw* we reccomend following along here as these excercises are designed to give you the building blocks 
for later usage.

All that being said .. lets dive in and see what we can do.

Currently in our apps/hello_world folder we should have a single file __init__.py. If you have copied an existing folder or 
renameed an exisrting example we reccomend deleting everything other than the __init__.py in order to follow this example.

Now that we have our directory structure sorted out lets get coding!!.

Before we dive in however there a number of differnt conventions that can be used for python projects. Looking at differnt covnetions is 
beyond the scope of this document and we suggest that your apps take on a structured approach with modules and sub folders.

To this end lets start off by creating a controllers.py to hold all of our **actions**.
::

    touch . controllers.py

Then lets open **controllers.py** in the editor of choice and add the following code.
::

    ### controllers.py ###

    from websaw import DefaultApp, DefaultContext
    import ombott
   
    ombott.default_app().setup(dict(debug=True))
    class Context(DefaultContec):
        ...

    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)

    @app.route('index')
    def hello_world(ctx: Context):
        return 'Hello Websaw World'

*So what is going on here?*

First we import our **App** and **Context** base clases from *Websaw* along with the **ombott** (One More Bottle) package. 
More inofrmation on bottle can be found at `The Official Bottle Site <https://bottlepy.org/docs/dev/>`_

Next we create our **Context** class using the imported **DefaultContext** as our base class and pass it to our app intitiliser

As we dont need anything else for now the default context is fine. In later chapters you will see how we can customise and leverage 
the **Context** in order to make our applications extremely flexible yet super secure.

Next we set up our app using the **DefaultApp**

.. note:: 

    All the above could be done in any other module and imported but for the sake of readablilty lets keep it all here for now.

    **example:** If you have an app with multiple modules we suggest you create a common.py module where all initialisation is done 
    then you can simply imprt what you need into each module but more on that later.

Then we get to our actual **action**.

.. important:: 

    For the sake of clarity an **action** in *Websaw* is deemed to be a **routeable function**

The first thing we need to do is declare our **route**. This lets our app know where to find the function **hello_world**.

There will be a lot more on **Routes** later on but for now lets just register a route called 'index'

.. note:: 
    
    We do not need seperate routing tables setup. This is all done by *Websaw* under the hood.


Followd by our function decleration. Once again it is important to note that the route and function names need not be the same.
In this case as we only have one function in our module it is easier to register our route as **index** as you will see later.

.. important:: 
    
    All **actions** in *Websaw* take context as a mandatory first argument

and all that ourt **action** now needs to do it return our 'Hello Webasw World' string.

Before we can actually run the application there are a few more things we need to do 

You can close and save controllers.py and open __init__.py

.. note:: 

    Once aganin we could probably have all this code in a single module but as your app grows it becaomes paramount to have things structured.

Add the following:
::

    ## __init__.py ##
    
    from .controllers import app

    app.mount()

The above should be pretty self expanatory in that we import our **app** instance from our controllers.py and then 
then mount our app using **app.mount()**

You can now save and close the __init__.py

Thats it .. lets check it out.

In your terminal run the following:
::

    python -m websaw run apps

head over to your browser and 
::

    http://localhost:8000/hello_world

All things being well you should see the reults of your very first *Websaw* app

Not very exciting and not very pretty but the foundation for things to come.

.. note::

    We declared our route as 'index' in our app but not on our URL. *Websaw* automatially defaults to /index
    if forget to add it and in effect http://localhost:8000/hello_world and http://localhost:8000/hello_world/index
    are equivalent

Well done .. you are now ready to see what *Websaw* can really do!!

