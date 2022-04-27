.. _fixtures:

========
Fixtures
========

As described in the :ref:`design_overview` section, **Fixtures** are *Websaw's* basic building blocks.
They can act as middleware (e.g. auth barrier or render routing action results using template)
**OR** as services (e.g. provide database connections) or a combination of the two.

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

To see a real fixture in action why not head on over to the `Websaw Workshop <https://websaw-workshop.readthedocs.io/en/latest/intermediate.html>`_
