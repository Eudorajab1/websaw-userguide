Working with data
-----------------

An important aspect of most **web applications** is the abitlity to access and process data, whether they be **client** or **server** side 
applications.

There are a myriad of database engines available these days and it is left to the developer to chose their preferred database engine 
for data storage and retrieval.

In order to provide maximum flexibility regarding database choice, **Websaw** ships with the **voodoodal** application which 
extends the standard PyDAL library to give additonal functionality and flexiblity when it comes to the **DAL**.

What is a DAL?
..............

The DAL or **Data Access Layer** dynamically generates SQL in real time using the specified dialect for the database back end, so that you do not have to
write SQL code or learn different SQL dialects. 

The term SQL is used generically and the application will be portable between different types
of databases.

Supported database engines
..........................

Here is a list of the database engines that  **Websaw** supporsts as standard:

==========  ==========================================
Database    Drivers (source)
==========  ==========================================
SQLite      sqlite3 or pysqlite2 or zxJDBC (on Jython)
PostgreSQL  psycopg2 or zxJDBC (on Jython)
MySQL       pymysql or MySQLdb
Oracle      cx_Oracle
MSSQL       pyodbc or pypyodbc
FireBird    kinterbasdb or fdb or pyodbc
DB2         pyodbc
Informix    informixdb
Ingres      ingresdbi
Cubrid      cubriddb
Sybase      Sybase
Teradata    pyodbc
SAPDB       sapdb
MongoDB     pymongo
IMAP        imaplib
==========  ==========================================

.. important:: 

    Do make sure that the correct driver for you preferred db engine is installed before tyring to connecto to the db.


So why voodoodal?
.................

**Voodoodal** allows us to extend our **DRY** coding philosophy to the **DAL**. We define a model once and can use it 
in all applications.

What is more we can **merge** multiple models to create fully functional databases simply by importing the models we are interested in 
and intialising the **new** database.

**Voodoodal** is designed to work with **mixins** to provide complete functionality and flexibitlty for our applications.

Voodoodal in action
...................

In order to better understand the power and flexibility of **voodoodal** lets take a look at it in action.

Before we look at some real life examples lets take a look at the structure of a typical **model** in detail.

Model definition
................

Lets create a demo model in demo_model.py
::
    # demo_model.py

    from voodoodal import Table, Field
    from pydal import DAL
    import datetime

    now = datetime.datetime.now()


    class sign_created(Table):
        created = Field('datetime', default=now)
        created_by = Field('reference person')


    class sign_updated(Table):
        updated = Field('datetime', default=now)
        updated_by = Field('reference person')


    class Model(DAL):

        __config__ = {
            # prefixes `rname` of all tables
            'prefix': 'test_',

            # add `primarykey = ['id']` if there is `id`-field with type != 'id'
            # see `color`-table below
            'auto_pk': True,
        }

        class person(Table):
            name = Field('string', required=True)

        class color(Table):
            id = Field('integer')
            name = Field('string', required=True)

        # to inject signature(s) just specify them as base class(es)
        class thing(sign_created, sign_updated):

            owner = Field('reference person', required=True)
            name = Field('string', required=True)

            @property
            def owner_id(row):
                """Define another virtual field."""
                return row.thing.owner

            @property
            def owner_thing_name(row):
                """Define virtual field."""
                return [row.thing.owner, row.thing.name]

            def owner_name_meth(row):
                """Define method field."""
                return [row.thing.owner, row.thing.name]

            @classmethod
            def get_like(self, patt):
                """Define table-method.

                This will turn into `db.thing.get_like(<pattern>)`-method.
                """
                db = self._db
                assert self is db.thing
                return db(self.name.like(patt)).select()

            # hooks goes as is

            def before_insert(args):
                print('before_insert', args)

            def before_update(s, args):
                print('before_update', s, args)

            def after_update(s, args):
                print('after_insert', s, args)

            @classmethod
            def _on_define(cls, t: Table):
                """Postprocessing hook."""
                print(f"_on_define: table '{t}' created")

            __extra__ = ['whatever']

        # special hooks
        def on_action(tbl, hook, *args):
            """Convenient common hook for all before/after_insert/update/delete actions."""
            print('on_action', tbl, hook, args)

        @classmethod
        def on_define_table(cls, tcls, t):
            """Postprocessing hook, invoked for each table."""
            print(f"on_define_table: table '{t}' created from {tcls}")

        @classmethod
        def on_define_model(cls, db: DAL, extras: dict):
            """Postprocessing hook."""
            print('on_define_model', db, extras)

As we can see the above is an example showing the ability of **voodoodal**. The code itself should be self explanetory and the most 
important thing to note is that this is purely the model definition and can be used in any db as we will see next.

Creating the database
.....................

The database initilisation and creation is normally done in a seperate module which allows us to store our **model** definitions seperately (normally in a common folder),
to make them available to other applications that may wish to use them.
::
    # demo_test.py

    from voodoodal import ModelBuilder
    from pydal import DAL
    import os

    from demo_model import Model

    _db = DAL(
        folder=f'{os.path.dirname(__file__)}/db_test'
    )


    # All magic goes here
    @ModelBuilder(_db)
    class db(Model):
        pass


    assert db is _db
    db.commit()

.. important:: 

    As the **DAL** supports a number of database engines as standard, the same database dfinition (**model**) can be used irrecpective of 
    database engine. The only thing that needs to change will be the connection string to your database engine of choice.

As our **Model** is engine agnostic is is common practice to develop our apps using one db enngine then switch engines
once we move to production. As can be seen from the examples we are typically using **SQLite** as our dev engine but can easily
switch to any of the supported db engines using the same models.

Thats it. We can of course run other checks and tests and even insert data to make sure the db was created correctly etc but in essense we have created and 
connected to our database of choice so lets run a few tests.
::
    # test.py
    ...

    # check signatures
    assert {db.thing.created, db.thing.created_by, db.thing.updated, db.thing.updated_by}.issubset({*db.thing})

    # check rname prefix
    assert all(t._rname == f'test_{t._tablename}' for t in db)

    # check auto_pk
    assert db.color._primarykey == ['id']


    john = db.person.insert(name='John')
    db.thing.insert(owner=john, name='ball')
    assert db.thing.get_like('ball%')[0].name == 'ball'
    db.thing(1).update_record(name='big ball')
    row: Model.thing = db(db.thing).select().first()

    assert row.owner_thing_name == [row.owner, row.name]
    assert row.owner_id == row.owner
    assert row.owner_name_meth() == [row.owner, row.name]
    assert db.thing.get_like('big%')[0].name == 'big ball'


Using multiple models
.....................

In order to use multiple models in our database we simply import them and add them to the class db(...) as such.
::
    ...

    @ModelBuilder(_db)
    class db(Model1, Model2, Model3, ...):
        pass
    ...

.. important:: 

    Models with the same table names will be **merged** in order to create a unified db.

    Data naming conventions should be followed in order to ensure the required results.

Now that we have seen how to define and create our database the **next** section will cover the standard 
**Websaw** **grid** classes which are the typical way for displaying and sorting dtat from our tables. 
