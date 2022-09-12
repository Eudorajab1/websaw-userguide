.. _server_side:

========================
Server Side Applications
========================

Server Side or **Traditional** web applications have been around for a while now and fundamentally leverage on 
an application server or servers (normally web servers) to process any requests from the client which are passed on to the 
*backend* application which does the bulk of the work including the rednering of the output or *response* to the clinet
which is then sent back to the requesting browser via the web server.

Web applications that need to access large amounts of data and perform complicated processes based on user input 
or queries generally tend to emplay this client/server approach for a whole host of reasons that are beyond the scope of 
this document, not least of which is a clear decoupling of the UI and data layers of the application.

While most **Traditional** python based web frameworks offer some form of re-usable code fucntionality at the application 
level leveraging on differnt base clasesses which the developer can sub-class, up until **WebSaw** there has not been
an easy way to create re-usable components that any or all applcations can have access to (similar to Vue components).

This genreally has meant a lot of code duplicaiton particularly at the UI level which in turn leads to poor maintainablilty 
and difficultiy during enhancements and upgrades.

**WebSaw** effectively addresses these shotcomings by allowing developers to create sets of re-usable components both for response renedering as 
well as providing **mixin** functionality *out of the box* which allows us to develop one particular application that can be used 
by all others on the same domain.

Furthermore **WebSaw** allows logged in users to access multiple applications without having to logout and log in to each 
individual application as *standard* and much much more.

Server Side Getting Started
---------------------------

If you have followed the Installation installation procedures as outlined in the Getting Started section you should already have
an apps folder with a number of sample apps that ship with **WebSaw** installed.

In this section of the user guide we will be focussing on the scaffold app that ships with **WebSaw** as standard and 
will walk through the most relevant parts of the scaffold application in order to understand how it all 
hangs together.

In order to test this simply open up your browser or click on http://localhost:8000/scaffold

If all is good you will see the scafold app index page or entry point so lets start from there.

If not please refer back to the :ref:`installation_label` section to see if you have missed any steps.

The Scaffold App
................

.. note::
    This application has been included to demonstrate the different areas of fucntionality that make up a **WebSaw**
    **Traditional** web application and can be used as a template for further applications. We leave the UI styling 
    up to the user to implement depending on preference.
    

So lets take a look at our scaffold app. You should also make sure that you have the mixins folder in your apps
directory as our scaffold also demonstrates the use of a mixin called info which we look at in more detail later.

For now lets start at the beginning and take a look at our controllers.py 
::
    import os

    from websaw import DefaultApp, DefaultContext, Template, Reloader
    from websaw.core import Fixture
    from websaw.fixtures import Env
    import ombott

    from ..mixins import info
    from . import utemplates as ut

    ombott.default_app().setup(dict(debug=True))


    # make a simple custom fixture that uses another fixture (session)
    class LastVisited(Fixture):
        def take_off(self, ctx: DefaultContext):
            session = ctx.session  # magic goes here - we touch session and ctx activates it!
            last_visited = session.get('last_visited', [])
            last_visited.append(ctx.request.path)
            last_visited = last_visited[-5:]
            session['last_visited'] = last_visited


    # extend default context with our fixture and info-mixin context
    class Context(info.Context, DefaultContext):
        track_visited = LastVisited()
        welcome_templ_overwrite = Template('welcome.html')
        env = {
            'foo': 'foo_value',
            'templ_dir': Reloader.package_folder_path(__package__, 'templates')
        }


    ctxd = Context()
    app = DefaultApp(ctxd, dict(group_name='websaw_apps_group_one'), name=__package__)

    # use mixin(s)
    app.mixin(info.app)


    @app.route('index')
    @app.use(ctxd.track_visited)  # note there is no session, but it used!
    def index(ctx: Context):
        ret = {
            k: ctx[k]
            for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
        }
        ret['app_data_keys'] = [*ctx.app_data.__dict__]
        ret['env'] = ctx.env
        return ret


    @app.route('set_env')
    @app.use(Env(foo='change foo value', bar='bar value'))
    def set_env(ctx: Context):
        return ctx.env


    @app.route('session')
    def session(ctx: Context):
        ret = {
            'group_session_data': {**ctx.group_session},
            'session_data': {**ctx.session},
            'local_data_keys': [*ctx.session.data.__dict__],
        }
        return ret


    # reuse mixin template
    @app.route('reuse_welcome_template')
    @app.use(ctxd.welcome_templ)
    def app_welcome(ctx: Context):
        return dict(msg='Hey! This is message from app controller')


    @app.route('upytl-demo')
    @app.use(ut.upytl_demo)
    def upytl_demo(ctx: Context):
        return dict(msg='Hey! This page is rendered using UPYTL')


    # let's go to:
    # http://127.0.0.1:8000/scaffold
    # http://127.0.0.1:8000/scaffold/index
    # http://127.0.0.1:8000/scaffold/session
    # http://127.0.0.1:8000/scaffold/reuse_welcome_template
    # http://127.0.0.1:8000/scaffold/upytl-demo

    # provided by mixin
    # http://127.0.0.1:8000/scaffold/welcome
    # http://127.0.0.1:8000/scaffold/welcome_template_overwritten
    # http://127.0.0.1:8000/scaffold/info/app

Whilst this may seem to be quite a lot to take in at once lets break it down into sections and cover off each section as we go.

The first thing we see after the mandatory imports and app initialisation is the creation of a custom **Fixture**

Using Fixtures
..............

*Websaw* has a number of "out of the box" fixtures which we can subclass or extend in order to generate 
specific functionaltiy or *Custom Fixtures* that we may need within the context of our application. 

These are all detailed extensively in the :ref::`fixtures` section of this user guide.

For now the important things to note about **Fixtures** are as follows:

  * they are only initialised when required (on the fly).
  * they are context specific and can comprise of other fixtures.
  * they are completely thread safe and secure.

So lets go ahead and take a look at our *Custom Fixture*
::
    # apps/scaffold/controllers.py

    class LastVisited(Fixture):
        def take_off(self, ctx: DefaultContext):
            session = ctx.session  # magic goes here - we touch session and ctx activates it!
            last_visited = session.get('last_visited', [])
            last_visited.append(ctx.request.path)
            last_visited = last_visited[-5:]
            session['last_visited'] = last_visited

We create our custom fixture called LastVisited based on our Fixture base class and focus on only the take_off method.

This means when we exit any *action* that uses our fixture we will trigger the fixture and do whatever we have defined in the take_off method.

In the above case we are just updating a counter stored in our local session to reflect the mumber of visits.

The Context Layer
.................

Next we look at how we get our fixture to work within our local context
::
    # extend default context with our fixture and info-mixin context
    class Context(info.Context, DefaultContext):
        track_visited = LastVisited()
        welcome_templ_overwrite = Template('welcome.html')
        env = {
            'foo': 'foo_value',
            'templ_dir': Reloader.package_folder_path(__package__, 'templates')
        }


    ctxd = Context()

We wil come back to what info.Context does in the **Mixins** section as well as the env decleration 
but for now lets focus on our fixture.

As you can see from the above we declare our local or *Design* context as ctxd and then include all the mixins, fixture and whatever else
we intend to use in our application.

The Application layer
.....................

This is typically where the majority of our code will go for each fucntion that our applciation is going to use.

As you can see from the above there are a number of actions declared but lets just focus on index for now.
::
    @app.route('index')
    @app.use(ctxd.track_visited)  # note there is no session, but it used!
    def index(ctx: Context):
        ret = {
            k: ctx[k]
            for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
        }
        ret['app_data_keys'] = [*ctx.app_data.__dict__]
        ret['env'] = ctx.env
        return ret

The above snippet is effectively declaring and registering the route 'index' with our application.

.. note::
    There is no need to have a seperate routing table in order to declare routes. This is all done autmatically
    by **WebSaw** under the hood and any conficting or duplicate routes will raise the appropriate error message.

You will also not that we are using convenicne decorators to streamline our code and make it more readable.

We then tell our application to use our **custom fixture** for the index action.

.. note::
    The name of the function need not be the same as that of the route. In fact you can declare multiple routes pointing at the same function.
    It is also appropriate at this stage to point out that **ctx** is always the first paramater to any function declared in an action.

Our index action will then do whatever processing it needs to do whilst at the same time firing the fixture when we exit the fucntion.

.. important::
    Our custom fixture is only initalised when we **Exit** and not when we enter. This makes for extremely efficient 
    code and keeps our application lean and mean.

Using Mixins
............

All **mixin** functionality including templates, actions fixtures and databases as created by the 
**mixin** is immediately available to the **host** app.

**TBC**




