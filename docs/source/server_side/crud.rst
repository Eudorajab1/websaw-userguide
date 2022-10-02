Working with CRUD
-----------------

CRUD or **Create, Read, Update, Delete** is the backbone for any application that needs to access data.

Depending on **access roles** users should be able to perform the above fucntions in a user friendly and **intuitive** way. Whether it is placing 
and order on a web shop or adding a contact any interaction with the **DAL** needs to be available.

**Websaw** ships with **standard** CRUD functionality that can be tailored to individual requrements by adding your 
own styling etc.

As such there are two main **CRUD** classes namely **SQLGrid** and **SQLForm** both of which are extended classes of the 
**BaseGrid** and **BaseForm** classes.

Both **SQLFrom** and **SQLGrid** can be used totally independantly or jointly in order to create a comprehensive **CRUD** engine.

**Websaw** ships with a **sample_crud** app which we will now look at in some detail in order to see how this all hangs together.

The CRUD sample app
...................

As mentioned above this application is provided in order to demonstrate simple CRUD principles as utilised by **Websaw**.

As CRUD by definition works with some form of **database** layer lets start off by taking a look at the database model that we will be working with.

The database model
..................

As we saw in the previous section we first of all need to define our db model.

As we have so far steered clear of the ubiquitous **todo** application lets at least pay homage here and use its database for our CRUD example.
::
    # apps/sample_crud/tod_model.py
    
    import datetime

    from websaw import DefaultContext

    from voodoodal import Table, Field

    from pydal import DAL

    def get_time_stripped():
        fulltime = datetime.datetime.utcnow() 
        stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
        retval = stripped.replace("T"," ")
        return retval.replace("T"," ")

    class TodoModel(DAL):
        class todo(Table):
            item = Field('string', label='Todo Item')
            notes = Field('text', label = 'Notes to me')
            date_added = Field('datetime', default=get_time_stripped, readable=False, writable=False)
        
Next lets intialise our db and take a look at our **CRUD** app
::
    # apps/sample_crud/todo_db.py

    import os

    from websaw import DAL
    from voodoodal import ModelBuilder

    from .todo_model import TodoModel

    _db = DAL(
        "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
    )

    # All magic goes here
    @ModelBuilder(_db)
    class db(TodoModel):
        pass

    db.commit()


Now that we have our **database** set up and ready to go lets take a look at the SQLGrid class 


The SQLGrid subclass
....................

As with the simple grid we use the Grid baseclass to define our specific SQLGrid as follows:
::
    # apps/common/common_utils.py
    
    class SQLGrid(BaseGrid):

    """
        all methods relating to our spedic grid will be here
    """        
    
    def get_options(self, *args, **kw):
        
        # options expected by concrete upytl grid-component goes here
        # so we have common processing logic
        # but can adjust options to different upytl grid-components
        ...
        
The code for the above can be found and reviewed as it is pretty much self explanatory as such we will not go into it in too much detail 
here.

The important thing to note is that both our form and our grid have the get_options method which effectively provides the 
specific data formation expected by whatever from or grid we have decided to implement.

This gives developers the freedom to implement their own class of form or grid and are not tied to the standard **Websaw** classes.

As the **form** baseclass and **SQLForm** follow the same principles we shall move on to looking at the actual **crud_sample** application to see them in action.

The SQLGrid
...........

This is our typical entry point for our **CRUD** functionality and in essense provides us with the means of displaying all 
redords in a table and offering us the **CRUD** options for each individual record.

We are leveraging our **grid** on **datatables** and have extended it to include our **CRUD** functionality.

Make sure that **Websaw** is up and running and head on over to the apps/sample_crud app and you should see a grid representation of the todo database table as defiened.

You will also note that there are a number of action buttons to facilitate the crud functionality.

In order to understand this better lets take a look at our controller.
::
    # apps/sample_crud/controller.py

    @app.route('index')
    @app.use(gt.grid_template)
    def index(ctx: Context):
        db = ctx.db
        grid=SQLGrid(ctx, 'db', db.todo, upload=True, download=True, page_title='My Todos Grid')
        
        if grid().accepted:
            ## do some additonal processing here
            print('Grid is good')
        else:
            ## raise the appropriate errors
            print('Grid is bad')
        return dict(grid= grid.get_options())        

As is demonstrated by the above the creation of a grid is an extremely simple process as the majority of the work is being done
by the SQLGrid class itself.

The most important lines here are 
::
    ...
    db = ctx.db
    grid=SQLGrid(ctx, 'db', db.todo, upload=True, download=True, page_title='My Todos Grid')
    ...

    return dict(grid= grid.get_options())        

First we get our current db from our context.

We then intilaise our SQLGrid, passing in the arguements we require. In this case we are telling the grid that 
we want to work with a database called 'db', and in particular the table db.todo. We want upload and download fucntionality and we want our 
page_title to be 'My Todos Grid'

The only really importnat arguments are ctx, db and db.todo the rest are optional.

Likewise we could switch off actions by passing in the approriate arugments like creatable=False, viewable=False etc.

The crud actions fucntionality
..............................

This is a slightly more complicated action as it needs to deal with all our CRUD actions in addition to the **grid** actions like **uploading and downloading** tables so lets take a look.
::
    @app.route('actions', method=['GET', 'POST'])
    @app.use(gt.action_template)
    def action(ctx: Context):
        session = ctx.session
        
        query = ctx.request.query
        action = query.get("action")
        db = query.get('cdb')
        table = query.get('table')
        show_buttons=True
            
        if not action or not table:
            redirect(ctx.URL('index'))
        else:
            db = ctx.ask('db')
            form = SQLForm(db[table]) #intialise our form
            if action == 'create':
                if form.process(ctx, db, db[table], None).accepted:
                    if ctx.request.method == 'POST':
                        redirect(ctx.URL('index'))
            
            elif action == 'update':
                id = query.get('id', None)
                if not id:
                    redirect(ctx.URL('index'))
                todo = db(db[table].id == int(id)).select().first()
                
                if form.process(ctx, db, db.todo, todo).accepted:
                    if ctx.request.method == 'POST':
                        redirect(ctx.URL('index'))
        
            elif action == 'view':
                show_buttons = False
                id = query.get('id', None)
                if not id:
                    redirect(ctx.URL('index'))
                todo = db(db[table].id == int(id)).select().first()
                
                if form.process(ctx, db, db.todo, todo).accepted:
                    if ctx.request.method == 'POST':
                        redirect(ctx.URL('index'))
        
            if action == 'delete':
                id = query.get('id', None)
                if not id:
                    redirect(ctx.URL('index'))
                todo = db[table](id)
                if todo is None:
                    redirect(ctx.URL("index"))
                db(db[table].id == id).delete()
                db.commit()
                redirect(ctx.URL("index"))
            
            elif action == 'download':
                
                filename = settings.DOWNLOAD_FOLDER+'/'+table+'.csv'
                with open(filename, 'w', encoding='utf-8', newline='') as dumpfile:
                    dumpfile.write(str(db(db[table]).select()))
                redirect(ctx.URL("index"))

            elif action == 'upload':
                
                filename = settings.UPLOAD_FOLDER+'/'+table+'.csv'
                try:
                    with open(filename, 'r', encoding='utf-8', newline='') as dumpfile:
                        db[table].import_from_csv_file(dumpfile)
                    db.commit()    
                except Exception as e:
                    redirect(ctx.URL('index'))
                finally:
                    redirect(ctx.URL("index"))

            return dict(form_options = form.get_options(), show_button=show_buttons)

As can be seen from the above the action is broken down into different based on the paramters passed in on the query.

In all instances relating to the *CRUD* we use the SQLForm class which allow us to perform the appropriate action

We therefore intialise our SWLform as such:
::
    form = SQLForm(db[table]) #intialise our form
            
which is then used by the actions and additonal arugumetns passed to the SQLFrom depending on the type of action we are working wiht.

The SQLForm in action
.....................

To demonstrate this take a look at the diffence between the 'create' and 'update' actions in our action.
::
    if action == 'create':
        if form.process(ctx, db, db[table], None).accepted:
            if ctx.request.method == 'POST':
                redirect(ctx.URL('index'))
            
    elif action == 'update':
        id = query.get('id', None)
        if not id:
            redirect(ctx.URL('index'))
            todo = db(db[table].id == int(id)).select().first()
            
        if form.process(ctx, db, db.todo, todo).accepted:
            if ctx.request.method == 'POST':
                redirect(ctx.URL('index'))
        


As we can see the 'create' action only needs to pass in the db.todo table whilst the 'update' action needs to pass in the 
db.todo table along with the record id (todo) that we want to update.

Another important think to note is that we are checking to see what type of request.method is being used.

If it is a 'GET' we return the initialised form whereas if it is a 'POST' it generally means the form has been processed and we should move on.

``form.process().accepted`` will return False if there are any errors on the form and these will be displayed as normal form errors
till the form is accepted.

Once again we will return our form.get_otions in order to ensure that the correct data is passed back to our componenets based on the type
of data we are processing.

And that is it for CRUD. You can use it **out-of-the-boy** for most applications but there is always the ability to customise or create your 
own form or grid classes as required.

.. important:: 

    Both the SQLForm and SQLGrid can be used totally independantly although in the case of SQLGrid it may be better
    to use just a standard grid for dipsplaying table records where no CRUD is required.

    You should also note the striking similarities between the **SimpleGrids** and the **CrudGrids** in terms of 
    utilisation and intialisation and the extremely small code footprint required in our controllers.

