Using mixins
------------

.. important:: 

    **Mixins have to be one of the most innovative and time saving features of Websaw**

So what is a mixin?
...................

In essence a **mixin** can be anything that you could use in any other application. 

This can range from a simple generic action (such as a logger) to an application itself.

In order to understand **mixins** lets take a look at the **simple** application that ships as 
standard with *Websaw* and see how it all fits together.

The first thing that we need to note is that by convention in our apps directory structure we have a
folder called **mixins** and yes you guessed it .. this is where we store our **mixins**.

The only real difference between **mixins** and **apps** is that we do not mount our mixins. 

Instead the **host** application will mount the **mixin** or even multiple **mixins** as part of its 
own **mount()**.

All **mixin** functionality including templates, actions fixtures and databases as created in the 
**mixin** are available to the **host** app once mounted.

**Websaw** ships with a number of standard mixins which you can use *out-of-the-box* which we will cover briefly at the end of this 
section and in greater detail in following sections. For now lets focus on the ``apps/mixins/info`` mixin.

So lets take a closer look:


The info mixin
..............

The objective of this app is to demonstrate the basic use of a **simple** mixin whist at the same time demonstrating some of the 
more advanced features like template overwriting and sharing between host and mixin.
::
    # apps/mixin/info/controllers.py

    import os
    from websaw import DefaultApp, DefaultContext, Reloader
    from websaw.templates import UTemplate
    from . import utemplates as ut

    class Context(DefaultContext):
        env = {
            'default_template_context' : dict(user = 'Test User'),
        }
        
        # To make template replaceable/referenceable we should assign a fixture key (e.g. welcome_template)
        # To do that use the following syntax for template:
        # <fixture_key>:UTemplate(<template>)

        welcome_template = UTemplate(ut.welcome)

    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)


    @app.route('welcome')
    @app.use(ut.welcome)
    def welcome(ctx):
        msg = (
            'Hey! this is a message from the info-mixin controller'
            'It uses the mixin welcome template'
        )
        return dict(msg=msg)

    @app.route('mixin_template_overwritten')
    @app.use(ctxd.index_template)
    def welcome(ctx):
        msg = dict(mixin_message = 'Hey! this is a message from the info-mixin controller'
                                    'It is using the main app index template'
        )    
        return dict(msg=msg)


    @app.route('info/app')
    @app.use(ctxd.index_template)
    def info_app(ctx: Context):

        def rep(v):
            if isinstance(v, list):
                return [rep(_) for _ in v]
            if isinstance(v, str):
                return v
            return repr(v)

        ret = {
            k: rep(v) for k, v in ctx.app_data.__dict__.items()
        }
        ret['env'] = ctx.env
        ret['ctx_fixtures'] = {k: repr(f) for k, f in ctx._fixt.items()}
        
        return dict (msg = ret)

.. important:: 

    By convention our mixins should **NOT** have an **index** route as it will conflict with the host or 
    main app 'index' route.

    Try to use routes that describle the functionality of the action as a general rule of thumb as it makes your code a lot 
    easier to understnd.

From the above we can see our **info** mxin has three actions to perform. The first is the **welcome** action which 
returns a simple welcome message.

The second demonstrates how the **main or host** app can override the mixin template (i.e get the mixin to use the **host** template instead of its own)

And the third action ``info/app`` returns low level information relating to the application.

If we take a closer look at the ``@app.use(...)`` decorators in all three actions you will notice that they differ somewhat.

Whilst the **weclome** route is using ut.welcome (which is explicitly the mixins **welcome** template), the other two
actions are using templates as defined in the contxt. Namely ``ctxd.index_template``

As there is no such template in our **mixin** we are explicitly telling our action to use the host template as per the 
``index_template = UTemplate(ut.welcome)`` in our local **Context** definition.

.. note:: 
    
    As mentioned in earlier sections the **Context** of the mixin is its entirety is available to the mixin and vice versa.

    The main thing we need to do here is to make sure there is a **context key** that both the host and the mixin can use to reference
    the appropriate functionality required.

    In this case we reference  ``index_template = UTemplate(ut.welcome)`` which we link to our local 
    welcome template (ut.welcome) in order to use the host **index** template instead of our local **welcome** template.
    
    In simple terms  **index_template** will overwrite the **welcome** template as the host always takes priority over the mixin and as **index_template** is defined in the 
    **host context** as the host's **index** template 

So now that our **mixin** is set up lets take a look at how we can use our **mixin** in our application.

The basic app
.............

The **basic** application has been included to demonstrate the use of **mixins** and in particular the **info** mixin as detailed above.

It also introduces the **auth** mixin and **group sessions** which both ship with **Websaw** as standard. In addition we introduce **context environoment** (**env**)
all of which we will be covering in the next sections.

The main aim however is to demonstrate the use of multiple mixins in a single host application with the emphasis on using in particular 
host templates from the mixin and vice versa so that is what we will be focussing on first.

So lets take a look at the **basic** appliction which is located at ``apps/basic``. 
::
    from websaw import DefaultApp, DefaultContext
    from websaw.core import Fixture
    from websaw.fixtures import XAuth
    from websaw.templates import UTemplate
    import ombott

    from ..mixins import info, auth
    from . import utemplates as ut

    ombott.default_app().setup(dict(debug=True))

    class GetUserMenus(XAuth):
        
        def take_on(self, ctx:DefaultContext):
            navbar = ctx.navbar
            user = ctx.current_user.user
            ctx.env['default_template_context']['menu'] = [
                {'label': 'Home', 'href':ctx.URL('index')},
                {'label': 'About', 'href':ctx.URL('about')}
                ]

    menu=GetUserMenus()

    class Context(info.Context, auth.Context, DefaultContext):
        env={
            'menus' : [],
            'menu': [],
            'default_template_context': dict(user = ''),
            'default_template_context': dict(buttons = ''),
            
        }
        index_template = UTemplate(ut.index)
        menu=menu

    ctxd = Context()
    app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

    # use mixin(s)
    app.mixin(info.app, auth.app)

    @app.route('index')
    @app.use(ctxd.menu, ctxd.index_template)  # note there is no session, but it used!
    def index(ctx: Context):
        user=ctx.current_user.user
        flash = ctx.flash
        ret = {
            k: ctx[k]
            for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
        }
        ret['app_data_keys'] = [*ctx.app_data.__dict__]
        ret['env'] = ctx.env
        ret['ctx_fixtures'] = {k: repr(f) for k, f in ctx._fixt.items()}
        return dict(msg=ret)

    @app.route('about')
    @app.use(ctxd.menu,ut.about) 
    def about(ctx: Context):
        ret = dict(mixin = 'http://127.0.0.1:8000/basic',
                    index = 'http://127.0.0.1:8000/basic/index',
                    welcome='http://127.0.0.1:8000/basic/welcome',
                    session='http://127.0.0.1:8000/basic/session',
                    use_mixin_template='http://127.0.0.1:8000/basic/use_mixin_template',
                    template_overwrite= 'http://127.0.0.1:8000/basic/mixin_template_overwritten',
                    info= 'http://127.0.0.1:8000/basic/info/app'
                    )
        
        return dict(msg=ret)

    # Use the  local 'private' index template implicitly
    @app.route('session')
    @app.use(ut.index)
    def session(ctx: Context):
        ret = {
            'group_session_data': {**ctx.group_session},
            'session_data': {**ctx.session},
            'local_data_keys': [*ctx.session.data.__dict__],
        }
        return dict(msg=ret)

    # use mixin template
    @app.route('use_mixin_template')
    @app.use(ctxd.welcome_template)
    def app_welcome(ctx: Context):
        return dict(msg='Hey! This is message from app controller using the INFO mixin template')


The first thing we need to do is to import the mixins that we want to use in or app as follows:
::
    ...
    from ..mixins import info, auth
    from . import utemplates as ut
    ...
Then include them in our **basic** application **Context**
::
    ...
    class Context(info.Context, auth.Context, DefaultContext):
    ...
        index_template = UTemplate(ut.index)
    ...    

Here we are extending our context **ctxd** with our **info** and **auth** mixin's **context** and providing our **context**
with the **context kex** index_template which now means that the physical template ut.index is referenced in our **context** by **incex_template**

And finally
::
    ...
    ctxd = Context()
    app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

    # use mixin(s)
    app.mixin(info.app, auth.app)
    ...

Before the app is mounted we add the **info.app** and **auth.app** to the app mixin propery and mount the app in the normal way.

With all the above in place we mount the app as normal in __init__.py and we are good to go.

The **actions** for the basic app should be self explanaatory so we will not get into them here.

For now make sure websaw is running and head on over to the basic app.

You will see the index page along wiht a menu with a Home and About option. What is more you should also see 
the functionalilty of the **user** mixin which will allow you to register and log in to the applicaiton.

If you select the **About** menu option you will see a list of links related to both the **basic** app as well
as the **info** mixin.

.. note:: 

    The paths to the mixin routes are exactly the same as if we had written one big applciation including all functionality.

    We can use templates from either **host** or **mixin** in either of them by setting specific **Context keys**.

    All **actions** in the **mixin** are available to the **host**
    
    **Mixins** are an **extremely powerfull tool**.


In the **next** section we will take a look at using the **group session** fucntionality. 

