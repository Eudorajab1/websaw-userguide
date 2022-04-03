.. _fixtures:

========
Fixtures
========

As described in the :ref:`design_overview` section, **Fixtures** are *Websaw's* basic building blocks.
They can act as middleware (e.g. auth barrier or render routing action results using template)
**OR** as services (e.g. provide database connections) or a combination of the two.

To get familiar with fixturies lets just create a slightly more usefull one than we we created in our 
:ref:`adding_a_fixture` section.

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

We are going to make the fixture equivalent of https://flask.palletsprojects.com/en/2.0.x/extensiondev/
as a comparison to those of you familiar with flask extensions.

So lets get going and create our **fixture**.
::

    # apps/sqlite3_demo/app_fixtures.py

    import sqlite3

    from websaw.core import Fixture

    class SQLite3(Fixture):
        def __init__(self, uri_or_fpath, **kwargs):
            self.uri_or_fpath = uri_or_fpath
            self.kwargs = kwargs

        def take_on(self, ctx):
            # self.data - thread safe local storage 
            conn = self.data.db = sqlite3.connect(self.uri_or_fpath, **self.kwargs)
            conn.row_factory = sqlite3.Row
            return conn

        def take_off(self, ctx: DefaultContext):
            db: sqlite3.Connection = self.data.db
            if ctx.exception:
                # there is some error(s) during action processing or/and
                # in other fixtures, so we don't want to save changes
                db.rollback()
            else:
                db.commit()
            db.close()


Now lets see how we can use it:
::

    # apps/sqlite3_demo/controllers.py

    import sqlite3

    from websaw import DefaultApp, DefaultContext, Reloader, HTTP
    from websaw.core import Fixture

    from .app_fixtures import SQLite3

    sqlite_db = Reloader.package_folder_path(__package__,  'demo_db.sqlite')

    # lets create the table in our db
    def init_db(sqlite_db):
        db = sqlite3.connect(sqlite_db)
        db.execute('CREATE TABLE IF NOT EXISTS thing(id INTEGER PRIMARY KEY, name TEXT)')

    init_db(sqlite_db)


    # extend default context with our fixture
    class Context(DefaultContext):
        # to get right autocomplete in action (e.g. when ctx.sdb.exe...)
        # we need to force IDE to think that cxt.sdb is type of sqlite3.Connection
        sdb: sqlite3.Connection = SQLite3(sqlite_db)

    ctxd = Context()
    app = DefaultApp(ctxd, name=__package__)

    @app.route('sdb')
    def sdb(ctx: Context):
        q = ctx.request.query
        action = q.get('action')
        if not action:
            cur = ctx.sdb.execute('SELECT * FROM thing')
            ret = [{**r} for r in cur.fetchall()]
        elif action == 'create':
            name = q.get('name')
            if not name:
                raise HTTP(429, 'Name is required')
            cur = ctx.sdb.execute('INSERT INTO thing(name) values(?)', (name,))
            ret = cur.lastrowid
        else:
            raise HTTP(400, f'Unkown action: {action}')
        return dict(result=ret)

And finally lets test it:
::

    # to insert any name into db
    http://127.0.0.1:8000/sqlite3_demo/sdb?action=create&name=John

    # to view all rows in db
    http://127.0.0.1:8000/sqlite3_demo/sdb

And thart is pretty much it.

The only limit to the usage of **fixtures** in your applicaitons is in your mind.
