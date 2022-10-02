Getting Started
===============

In this section will be looking at the basic building blocks for any **Websaw** application and 
will walk through the most relevant parts of some of the sample applications in order to understand how it all fits together.

Before we start lets make sure that we have everything installed correctly and the easiest way to do this is simply to open up your browser 
or click on http://localhost:8000/skeleton

If all is good you will see the skeleton app index page or entry point so lets start from there.

If you do not see the message from the sekeleton app please refer back to the :ref:`installation_label` section to see if you have missed any steps.

Application Anatomy
-------------------

Every **Websaw** application consists of three distinct parts.

    1. Fixtures - think of these as the individual services that the applicaiton will utilise
    2. Context - think of this as the services manager
    3. Application - the layer that uses the services and procides the application functionality

In order to see this in action lets take a look at the most basic of applicaitons that ships with **Websaw** apropriately called
**skeleton** which is basically a *bare-bones* application that demonstrates the above principle nicely.

.. important::
    
    The principles demonstrated by this application form the backbone for all future applicaitons.
    
    As such we **storngly** reccomend that you familiarise yourself with the funcdamentals before proceeding
    too much further.

So lets take a look at a typical **Websaw** application as outlined by the **skeleton app**. 

The **skeleton** app should be in your ``apps/skeleton`` folder of your **websaw** directory.


Application Directory structure
-------------------------------

The **reccomended** structure for a typical **Websaw** application is as follows:
::
    /apps
        /mixins
        /<app name>
            __init__.py
            controllers.py
            templates.py
            /databases
            /static
                /css

.. note:: 
    This is the reccomended directory structure for a typical **Websaw** application. You can of course tailor it to meet your own needs.

Now lets take a look at the above and break it down.

The first in the tree is the **mixins** folder and only requireed if you intend to use any mixins in any of your apps.

**Mixins** will be covered in a later section but for now you can think of them as being similar to Vue componenets.

**<app_name>** is the name of our application. In our case this will be **skeleton** as this is the app we will be looking at.

**databases** is the folder we we will store our dtat definitions and or database if our app requires database access

**static** is a reserved folder and is normally reservered for **css** or **js** or both and can also be used to store images etc.


The Controller
--------------

Typically called *controllers.py*, this file as the name suggests is used to initialise the applciation and define all the acctions needed by the **Application** layer
to provide the functionality we are going to include in our applciation.

.. note:: 
    There is no limit to the number of controller type files that you can have in your applciation procided that you register them in the __init__.py file in order
    as per standard python convention.

    Indeed there is no need to have a *controllers.py* file at all and you could just as easily put all functionlity in the ``__init__.py`` file.


Now lets take a look at our skeleton app.
::
    # /apps/skeleton/controllers.py

    from websaw import DefaultApp, DefaultContext
    import ombott

    ombott.default_app().setup(dict(debug=True))


    class Context(DefaultContext):
        ...


    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)


    @app.route('index')
    def index(ctx: Context):
        
        msg = 'Hello from skeleton app index'
        return dict(msg = msg)


As can be seen from the above we are using the **DefaultContext** and **DefaultApp** classes from websaw to define our application.

As this is pretty much a **bare bones** application we dont need anything else at the moment. In later sections we will add to this **bare bones** application

The main things to note is that we are setting up our application using **defaults**

We have a single route name **index** which is the typical entry point for any application which simply returns a message.

Mounting the app
----------------

Now that we have initialised out application we need to **mount** it in order for it to run.

This is done in the __init__.py as follows:
::
    # /apps/skeleton/__init.__py
    
    from .controllers import app
    app.mount()

And that is it. You now have a fully functioning **Websaw** application that is using the DefautltContext and DefaultApp functionality of **Websaw**.

We will now look at how we can add additional functionality to our apps in a secure and efficient way

In the next section we will be looking at **fixtures**
