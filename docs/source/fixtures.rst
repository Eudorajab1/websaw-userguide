.. _fixtures:

========
Fixtures
========

As described in the :ref:`arch_overview` section, **Fixtures** are *Websaw's* basic building blocks.
They can act as middleware (e.g. auth barrier or render routing action results using template)
**OR** as services (e.g. provide database connections) or a combination of the two.

The Base Fixture
................

To start with lets take a look at the **Fixture** base class:
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

As you can see there are 3 method-hooks to be overwritten:
    - app_mounted
    - take_on
    - take_off

Standard Fixtures
.................

**WebSaw** ships with a number of 'out-of-the-box' fixtures in order to get you up and running quickly and securely.

These fixtures can be used 'as-is' in the most part and in most cases there is little need to customise or modify these fixtures at all.

Whilst it is beyond the scope of this guide to examine each in turn the following provide a listing of the standard
fixtures that ship wtih **WebSaw**.

    * **DAL**           # data access layer 
    * **Session**       # all aspects of session management
    * **GroupSession**  # manages session agross multiple apps
    * **Env**           # fixture to manage environemnt in context
    * **Template**      # deals with all aspects of template rendering 
    * **URL**           # fixture for managing reditects and much more
    * **XAuth**         # authorisation fixture
    * **CurrentUser**   # convenience fixture to get or set current user in session
    * **AuthGuard**     # guards agains unauthorised access


Customising Fixtures
....................

In order to better examine the power of **Fixtures** lets take a look at the xauth app that ships with
**WebSaw** as standard. 
::

    # /websaw/apps/xauth/controllers.py

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

In this example we see that we are creating our **Custom Fixture** based on the standard XAuth base fixture class which
is the **WebSaw** standard **Authorisation** class containing methods like the ones above that we will extend or customise 
for our own fixture.

The methods that will customise here are register(), user_by_login() and user_for_session().

.. note::
    We are storing our users{} information in a local dictionary in memory but we could very easliy extend this fixture to 
    store and retrieve user credentials form the database of our choosing. 

The above code should be pretty much self explanitory as we are simply extending the methods that we are going to use in our app.

All the rest of the methods in the XAuth fixture are available to us some of which we will just use as standard. 

Next we initialise our Auth fixture and use the register method to add some dummy data to our users dict as such:
::

    auth = Auth()

    auth.register(dict(
        id=1,
        name='Tom',
        password=auth.crypt('tom_pass'),
        is_blocked=False,
        email='tom@qq.com'
    ))

    auth.register(dict(
        id=2,
        name='Kevin',
        password=auth.crypt('kevin_pass'),
        is_blocked=False,
        email='kevin@qq.com'
    ))

    auth.register(dict(
        id=3,
        name='John',
        password=auth.crypt('john_pass'),
        is_blocked=True,
        email='john@qq.com'
    ))

The main thing to note here is that the password field is being intialised using auth.crpyt which is a method of your 
base class *XAuth* and we have opted to use it without customising it.

The next steps are standard for all **WebSaw** applications where we extend the **Default** context with our 
**auth** fixture and initialise our application using our extended design contexct **ctxd**
::

    # extend default context with our fixture
    class Context(DefaultContext):
        auth = auth

    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)


Now we are ready to create the actions that will use our custom **auth** fixture as follows:
::

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

Here we have created three actions as above along with registering our routes with our **WebSaw** application. 

The login() and logout() actions are pretty straight forward but if we look at the last action we will see 
that we are telling our action to use another of the **Default** fixtures calle **auth_guard**.

This **Fixture** is available in the 'DefaultContext' and as such is available to all actions in all applications
based on our **DefaultContext** which in our case was extended with our custom auth() fixture.

Finally do not forget to mount the app
::

    # websaw/apps/xauth/__init__.py
    from .controllers import app

    app.mount()

To see this app in action sure that **WebSaw** is running then visit the following in your browser along with the expected results.
::

    http://127.0.0.1:8000/xauth/login?login=tom&pw=tom_pass #OK
    http://127.0.0.1:8000/xauth/login?login=kevin&pw=tom_pass #401
    http://127.0.0.1:8000/xauth/login?login=john&pw=john_pass #403

More on Fixtures
................

Fixtures are extremely flexible and powerfull building blocks that allow us to develop code quickly and efficiently.

We storngly reccoemend that you familiarise yourself with their uses and potential in order to save a significant amount
of time longer term.

To see more paractical examples of fixture use you should head on over to the `Websaw Workshop <https://websaw-workshop.readthedocs.io/en/latest/intermediate.html>`_
