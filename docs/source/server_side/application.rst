The Application Layer
---------------------

The **Application Layer** or **app** is where the majority or our work will be done. As the name suggests
it is effectively where we build the functionality of our application and normally consists of a corntollers.py or a number
of python modules which will contain all the functions and actions required by our application.

So what is the application layer?
.................................

The **Application** layer is responsible for collecting routes along with mounting and wrapping each action by 
route handler with the correct setup/teardown procedures.

Using the Fixture
.................

Now that we have defined and intialised our **custom auth fixture** lets put it to use in our application by including it in application initialisation
and letting the **app** know about it.

The first thing we need to do is to intialise then mount the application or **app**

This we do as follows:
::
    # apps/xauth/controllers.py
    ...
    app = DefaultApp(ctxd, name=__package__)
    ...

.. note:: 
    We are initialising our app by passing in cxtd (our **design** context) as a positional argument. There are a few other arguments which we will cover in later
    chapters but for now they are not required.

Not forgetting in our __init__.py to mount the app
::
    # apps/xaurh/__init__.py
    
    from .controllers import app

    app.mount()

At this stage we should have a fully functioning application that will use our custom **auth** fixture.

The Application
...............

Lets take a look now at our actual application which contains a number of routes or **actions**.
::
    # apps/xauth/controllers.py
    ...
    @app.route('login')
    def login(ctx: Context):
        q = ctx.request.query
        user, autherr = ctx.auth.login(q.login, q.pw)
        if user:
            redirect(ctx.URL('private'))
        return autherr.as_dict()


    @app.route('logout')
    def logout(ctx: Context):
        user = ctx.auth.user or dict(name="Guest")
        ctx.auth.logout()
        return f"Byе {user['name']}!"


    @app.route('private')
    @app.use(ctxd.auth_guard)
    def private(ctx: Context):
        return dict(user_in_session=ctx.auth_guard.user)


The important things to note here are:
  
    * We access our **auth** fixture as a property of **ctx** (our *Context*)
    * We dont need a sperate routing table for registering our routes. This is all done automaticlly *under-the-hood*
 
We could equally as well intialis a local **auth** in our action by doing somthing like which we can then use as ``auth.login(...)`` if we so desire. 
::
    ...
    auth = ctx.auth
    ...

.. note::

    A **route** indexes our **action** within the current **context** so calls to our **action** will be routed
    correctly in all cases.

    In order to simplify this and to avoid having to set up a seperate **routing table** we have the 
    **@app.route()** decorator which allows us to define a route for a paticular action.

    The **@app.use()** decorator is telling our action to use a particular fixture.


The **Auth** fixture is **NOT** triggered until we actually use it even though it is available at **take_on**. 

You will also notice that in the **private** action we are specifically telling our action to use the **auth_guard** fixture via the 
``@app.use(ctxd.auth_guard)`` decorator. The **auth_guard** fixture is one of the standard **Websaw** convenience fixture and as its name 
implies will prevent any access to any action that is **using** it if so desired.

We will be covering the ``@app.use(...)`` decorator in greater detail throughout later sections of this guide.

Although we did not include it in our **Context** definition is is autmatically available to us as it is part of the **DefaultConext** fixture.
As such we do not need to implicitly include it in our **Context**

Thats it .. we are good to go.

Make sure **Websaw** is running and follow the links below. You will see the appropriate error codes based on how the applicaiton logic.

=========================================================== ========================
URL                                                         Expected Response
=========================================================== ========================
http://127.0.0.1:8000/xauth/login?login=tom&pw=tom_pass     OK
http://127.0.0.1:8000/xauth/logout                          Bye Tom!
http://127.0.0.1:8000/xauth/login?login=kevin&pw=tom_pass   error 401
http://127.0.0.1:8000/xauth/login?login=john&pw=john_pass   error 403
=========================================================== ========================


Try to access the the private action without being logged in and see the result!

**next** we will take a look at **Component based templating**
