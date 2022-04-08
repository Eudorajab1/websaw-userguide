
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

As per tradition we are going to create a simple Hello World app to understnad the basics of the *Websaw* framewok 
after which we will get into a lot more depth and detail regarding the tools and techniques being used.

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


Followd by our function decleration. Once again it is important to note that the route and function 
names need not be the same.

In this case as we only have one function in our module it is easier to register our route as **index** as 
you will see later.

.. important:: 
    
    All **actions** in *Websaw* take context as a mandatory first argument

and all that ourt **action** now needs to do it return our 'Hello Webasw World' string.

Before we can actually run the application there are a few more things we need to do 

You can close and save controllers.py and open __init__.py

.. note:: 

    Once aganin we could probably have all this code in a single module but as your app grows it 
    becomes paramount to have things structured.

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

Using Templates
---------------

Templates are a tried and tested way to give your application a uniform *look and feel* whilst at the same
time allowing you to use one or more .css libraries for styling including your own custom styling.

If you are not familiar with html and css there are many excellent sites that can get you up to speed quickly and it 
is beyond the scope of this document to cover this.

That having been said lets jump into adding a bit of 'zing' to our otherwise drab and sad looking app.

The first thing we need to do is create a directory where we will be storing our templates. By convention we call this 
directory **templates** and create and empt __init__.py.

From within your hello_world directory run the following:
::

    mkdir templates
    touch templates/__init__.py
    cd templates

Now with your editor of choice create a new file called **app_layout.html** which we will use as our application
wide template.

Once open lets add the following:
::

    <!DOCTYPE html>
    <html>
    <head>
    <base href="[[=URL('static')]]/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="data:image/x-icon;base64,AAABAAEAAQEAAAEAIAAwAAAAFgAAACgAAAABAAAAAgAAAAEAIAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAPAAAAAA=="/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" />
    [[block page_head]]<!-- individual pages can customize header here -->[[end]]
    </head>
    <body>
    <header>
        <!-- Navigation bar -->
        <nav class="navbar is-light" role="navigation" aria-label="main navigation">
        <!-- Logo -->
        <a class="navbar-item " href="[[=URL('index')]]">
            <div class="icon-text">
              <span class="icon has-text-success">
                <i class="fas fa-home fa-lg"></i>
              </span>
              <span class="has-text-primary is-size-5 has-text-weight-semibold">Home</span>
            </div>
        </a>
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="my-navbar">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
        </a>
        
        <!-- Left menu ul/li -->
        [[block page_menu_items]]<!-- individual pages can add menu items here -->[[end]]

        [[block page_left_menu]][[end]]
        <!-- Right menu ul/li -->
        </nav>
    </header>
    <!-- beginning of HTML inserted by extending template -->
    [[include]]
    <!-- end of HTML inserted by extending template -->
    <footer class="footer is-small">
      <div class="content has-text-centered">
        <p>Powered by <strong>&nbsp;WEBSAW</strong> <a href="https://websaw.com"></a>
        </p>
      </div>
    </footer>
    </body>
    [[block page_scripts]]<!-- individual pages can add scripts here -->[[end]]
    </html>

Feel free to the styling library of your choide. Here we are using **Bulma** but we could equally well have used
**Bootstrp** or eve **no.css**. The choice is really yours.

You will also note we are using the cdn's which is again by choice. If you wanted to use local files you need to create a 
**static** folder in the hello_world app and create a **css** and **js** subfolder.

The most important thing to notice here is the **[[include]]** directive. We will extend all our templates (.html files) 
with this app_layout.html to give them a consitant and similar look and feel.

It also saves us the hassle of having to import libraries for every template we generate.

So .. now that we have our app layout sorted out .. lets take a look at what we can to do with our application.

We start by creating a new file called **index.html** which will extend the app_layout.html as follows:
::

    [[extend "app_layout.html"]]
    <div class = "container">
      <div class = "columns">
        <div class = "column has-text-centered">
          <div class = "notification is-primary">
            [[=msg]]    
          </div>
        </div>
      </div>
    </div>                


and that should be it.

.. note:: 

    [[=msg]] is the information that we will display on this page as proviced by our heelo_world function.
    
So lets head over to our controllers.py and see what we need to do.

The first thing we need to do is to tell our function to use the index.html template. We do this by adding the 
followng:
::

    app.use('index.html')

.. note:: 

    This should be declared after the route directive and before the function decleration


*Websaw* has a builtin **template fixture** that deals with initialising and rendering our index.html. 

We will be creating our own simple **fixture** next and cover **fixtures** in depth in the :ref:`fixtures` section.

In order for our template to render correctly we need to return a dictionary so we should update our function as
follows:
::

    return dict(msg = 'Hello Websaw World')

Our complete action should now look like this:
::

    @app.route('index')
    @app.use('index.html')
    def hello_world(ctx: Context):
        return dict(msg='Hello Websaw World')

Go ahead and run it 
::

    http://localhost:8000/hello_world

or just refresh your browser.

Starting to look a little bit better now. So much so in fact that we should consider notifying visitors on the 
number of times they have actually visited our application.

To do this lets create a very simple **Fixture**

.. _adding_a_fixture:

Adding a Fxture
---------------

*Websaw* has a number of "out of the box" fixtures which we can subclass or extend in order to generate 
specific functionaltiy that we may need within the context of our application. 

These are all detailed extensively in the :ref:`fixtures` section of this manual.

For now the important things to note about **Fixtures** is as foolows:

  * they are only initialised when required (on the fly).
  * they are context specific and can comprise of other fixtures.
  * they are completely thread safe and secure.

So lets get to it. Our objective is to create a simple *fixture* that will simply count the number of times a particular
browser has visited our site.

We can extend this later to store the results in a database of our chosing but for now we will use the session
to keep a count.

So lets get going.

The first thing we need to do is to import the Fixture base class from websaw.core
::

    from websaw.core import Fixture

Then we can define our new fixture called **Visited** as such:
::

    class Visited(Fixture):
        def take_on(self, ctxd: 'Context'):
            self.data.session = ctxd.session
            self.data.session['counter'] = ctxd.session.get('counter', 0) + 1
            
        def get_visits(self):
            return self.data.session['counter']

.. note:: 

    We will cover all the Fixture properties in the :ref:`fixtures` sectiom in detail. For now we are using the 
    take_on method to basically increment the session['counter']

We then add a fixture method called get_visits which we will use in our action to access our fixture data and include
it to our context.
::

    class Context(DefaultContext):
        visited = Visited()

In our action we now can use our new fixture simply by adding the folloing code
::

    visited = ctx.visited.get_visits()

where ctx is our **context**, **visited** is our **custom fixture** and **get_visits()** is our method.

and we simply add visted to the dictionary we are returning to the template
::

    return dict(msg='Hello Websaw World', visited=visited)

Now all that is left for us to do is to style and display the infomration in our index.html as such:
::

    [[extend "app_layout.html"]]
    <div  class = "container">
      <div class = "columns">
        <div class = "column has-text-centered">
          <div class = "notification is-primary">
            [[=msg]]    
          </div>
          </div>
            <div class = "column has-text-centered">
              <div class = "notification is-info">
                You have visited this site [[=visited]] times. Dont be a stranger!!    
              </div>
            </div>
        </div>
    </div>                


We could equally well access the ctxd.session object and increment it directly in our **hello_world** action 
but now **ANY** action using our **ctxd** that requires a count of the visits can access our **Visits** fixture or not
as the case may be.

Maybe not the most usefull of fixtures we will ever use but it should show the basic concept. If you think for example
of creating an authorization fixture then things become a lot more meaningfull.

Pretty neat stuff !!

So far we have seen how the three main layers of *Websaw* in action.
    
    * **Fixture**
    * **Context**
    * **Application**

You will also note that so far we have not mentioned things like **request**, **response** and **sessions** that make up any 
HTTP framework.

This does not mean that they are not there .. far from it. 

We will cover these in the **Context** section of the user guide but for now lets take a deeper look into **fixture** layer
by heading over to the :ref:`fixtures` seciton.

