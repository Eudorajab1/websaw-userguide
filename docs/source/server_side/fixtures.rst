Working with fixtures
---------------------

**Fixtures** are *Websaw's* basic building blocks.
They can act as middleware (e.g. auth barrier or render routing action results using template)
**OR** as services (e.g. provide database connections) or a combination of the two.


Anatomy of a fixture
....................

In order to better understand the anatomy of a **fixture** lets take a look at the **Fixture** class from which all
other fixtures are generated.
::

    class Fixture:

        # Central thread local storage to hold local data of all fixtures
        _local = threading.local()

        # Should the fixture be treated as a set of hooks - take_on/take_off.
        # If it is set to True, then 'take_off' method is called
        # regardless of whether 'take_on' method was called
        is_hook = False

        # The name of the fixture in the Context.
        # It is intended to be used in generic fixtures (e.g. Tempalte)
        # and supposed to be set in __init__
        context_key: Optional[str]

        @classmethod
        def initialize_safe_storage(cls):
            """Initialize the central thread local storage of all fixtures.
            We do it with one shot!
            """
            cls._local.fixtures_data = {}

        @classmethod
        def prepare_for_use(cls, fixture: 'Fixture'):
            """Initialize the thread local storage for concrete 'fixture'."""
            cls._local.fixtures_data[fixture] = SimpleNamespace()

        @property
        def data(self) -> SimpleNamespace:
            """Return the thread local fixture storage."""
            return self._local.fixtures_data[self]

        def app_mounted(self, ctx):
            """Is called when app is mounted."""
            ...

        def take_on(self, ctx) -> Optional[Any]:
            """Is called when the fixture is accessed as the context attribute.
            This hook is intended for the fixture initialization when it is accessed
            the first time during request processing.
            The return value is what the consumer will get when accessing the fixture
            as the context attribute. So it should return something useful
            e.g. opened file-descriptor or db-connection, if it returns None
            then the fixture itself will be used.
            The return value is cached in the context until take_off-hook is called.
            Note: This hook is only called if it's the request processing:
            @app.route('index')
            @app.use(ctxd.foo)  # won't be called as it's app loading stage
            def some(ctx):
                ctx.foo         # will be called as it's request processing
            """
            ...

        def take_off(self, ctx):
            """Is called at the end of request processing.
            if self.is_hook is set to False then it is only called if take_on-hook was called
            This hook is for cleanup/tear down action (e.g. to close a file or db-connection)
            """
            ...


As you can see there are 3 method-hooks that we can extend depending on the befhaviour required for **fixtures**

    - app_mounted
    - take_on
    - take_off

The **app_mounted** hook will fire when the application is mounted and is traditionally used to make database connections, load default data etc.

The **take_on** hook will fire when we enter and action that uses our **fixture**

The **take_off** hokk will fire when we exit our action

Standard Websaw fixtures
........................

**WebSaw** ships with a number of 'out-of-the-box' fixtures in order to get you up and running quickly and securely.

These fixtures can be used 'as-is' in the most part and in most cases there is little need to customise or modify these fixtures at all.

Whilst it is beyond the scope of this guide to examine each in turn the following provide a listing of the standard
fixtures that ship wtih **WebSaw**.

======================= ============================================================
Name                    Description
======================= ============================================================
**DAL**                 data access layer 
**Session**             all aspects of session management
**GroupSession**        manages session agross multiple apps
**Env**                 fixture to manage environemnt in context
**Template**            deals with all aspects of template rendering 
**URL**                 fixture for managing reditects and much more
**XAuth**               authorisation fixture
**CurrentUser**         convenience fixture to get or set current user in session
**AuthGuard**           convenience fixture to guards agains unauthorised access
======================= ============================================================
Creating a custom fixture
.........................

A typical use case for extending a *Base* fixture would be extending the **XAuth** fixture to proide bespoke 
*authorisation* funtionality for our applicaiton or applications.

**Websaw** ships with the **xauth** app which demonstrates the use of a *custom fixture* based on the **Xauth** standard **Webssw** fixture.

 .. important::
    The full code is in the **xauth** app in /apps/xauth and follows the same basic structure as the **skeleton** app.
    
    As such we will be focussing only on the parts not alreadfy covered in the **skeleton** app in order to avoid repetition.

So lets start by looking at the code and break it down as we go.

In addtion to importing *DefaultApp and DefaultContext* we import the **Xauth** fixture which we are going to use to define our **custom fixture** along wiht the redirect fixture which we will use in our application.
::
    # /apps/xauth/controllers.py
    
    from websaw import DefaultApp, DefaultContext, XAuth, autherr, redirect
    ...
    
    class Auth(XAuth):
        users = {}

        def register(self, fields):
            self.users[fields['id']] = fields

        def user_by_login(self, login: str) -> dict:
            login = login.lower()
            user = (u for u in self.users.values() if u['name'].lower() == login)
            return next(user, None)

        def user_for_session(self, user):
            suser = super().user_for_session(user)
            suser['email'] = user['email']
            suser['name'] = user['name']
            return suser

        auth = Auth()
        ...

As the **default** Xauth fixture will fire on **take_on** we will use the default hook in our **Auth** fixture.

In our **custom Auth fixture**  we Wwe define a number of methods that we want our **app** to use.
and indeed are using some of the *base Xauth* and in particular **user_for_session** using **super()** which gives us 
access to the methods in the **Xauth** base class. 

.. important:: 
    
    We are using some of the *base Xauth* and in particular **user_for_session** using **super()** which gives us 
    access to the methods in the **Xauth** base class. 

    We could just as easily define any additional functionality that we wanted here. The above is purely an example and should not be used in production.


Now that we have our **Auth** fixture set up and ready for action lets go ahead and take a look at how 
we can incorporate our *custom fixture* in our application.

In order to do this we should take a look at the **Context** layer next. 
