The simple grid
---------------

Websaw ships with a two basic types of grid. The *Datatables* grid and the *Html* grid.

Both are demonstraded in the ``apps/grid`` app which we well take a look at now.

All grids in **Websaw** are extensions of the **BaseGrid** standard class which ships with **Websaw**. 

While we will not go into the code in great detail we will take a loot at it. 

The BaseGrid class
..................

There are a number of arguments we can use to affect the behavour of our Grid as follows.
::
    """
    This is the Base Class from which all grids should be built. Any overrides should be done
    in specific classes
    """

    class BaseGrid:
        """
        Usage in websaw controller:

        def index():
            grid = Grid(db.thing, record=1)
            return dict(grid=grid)

        Arguments:
        - db name we are using as defined in DBRegistry must be a string
        - table: a DAL table or a list of fields
        - fields: a list of fields to display
        - create: set to False to disable creation of new record
        - editable: set to False to disallow editing of record seletion
        - deletable: set to False to disallow deleting of record seletion
        - links: list of addtional links to other tables
        - form_name: the optional name for this grid
        - serverside: set to False for client side processing
        - is_crud: set to False to disable CRUD options on the grid
        """

The main objective of the **BaseClass** is to provide common processing functionality for all grids and all derived or sub classes of the baseclass will
effectively extend or override methods in the baseclass for the required results.

The SimpleGrid class
....................

The Simple Grid is a non CRUD grid which is typically used to view records in a data table. Optional options would be to search and sort the data
and to give a nice visual display.

We offer both options as **standard** upytl components and they are included in the **upytl_standard** library that ships with **Websaw**

So lets start off by taking a look at the **grid defineiton**
::
    # apps/common/common_utilities.py
    
    class SimpleGrid(BaseGrid):
    
    def build_row_data(self, row):
        db = self.db
        table = self.table
        for col in self.fields:
            if db[table][col].type.startswith('reference'):
                row[col] = db[table][col].represent(row[col], row)
        return row

    def get_options(self, *args, **kw):
        
        # options expected by concrete upytl form-component goes here
        # so we have common processing logic
        # but can adjust options to different upytl form-components
        
        payload = {}
        self.tablename = self.table._tablename
    
        payload['title'] = self.page_title
        payload['grid_buttons']= []
        payload['columns'] = self.columns
        payload['labels'] = self.labels
        tablename = self.table._tablename
        payload['name'] = self.table._tablename
        
        rows = self.db(self.db[tablename]).select()
        data_rows=[]
        for row in rows:
            test = self.build_row_data(row)
            data_rows.append(row.as_dict())
        payload['data'] = data_rows
        return payload

The above initalises and releies on the **BaseGrid** class to do most of the heavy lifting. Important to note that we 
format the data into what the components(s) are expectiong before returning the payload.

The grid template
.................

As mentioned earlier this is part of the **upytl_standard** components library and as such is pretty simple to define.
::
    # apps/grid/grid_template.py
    
    from upytl import Slot, SlotTemplate, Component, html as h
    from upytl_standard import HTMLPage, DTGrid, HTMLGrid 

    grid_template = {
        HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Todo'):{
            SlotTemplate(Slot='nav'):{},
            SlotTemplate(Slot='flash'):{},
            SlotTemplate(Slot='content'):{
                h.Template():{
                    h.Div(Class="column"): 'This is a simple DT grid',
                    
                    DTGrid(
                        title={'grid.get("title")'}, 
                        name={'grid.get("name", "No Name")'}, 
                        grid_buttons={'grid.get("grid_buttons")'},
                        columns={'grid.get("columns")'},
                        labels={'grid.get("labels")'}, 
                        data={'grid.get("data")'}
                    ): {},
                },
                h.Template():{
                    h.Div(Class="column"): 'This is a simple HTML grid',
                    HTMLGrid(
                        title={'grid.get("title")'}, 
                        name={'grid.get("name", "No Name")'}, 
                        grid_buttons={'grid.get("grid_buttons")'},
                        columns={'grid.get("columns")'},
                        labels={'grid.get("labels")'}, 
                        data={'grid.get("data")'}
                    ): {},
                }
            }
        }
    }        

As the objective is to show both types of **grid** together you will see that we have both components in our template.

This would not normally be the case in a real life application and is purely here for the sake of comparison.

You will also notice that we import the DTGrid and HTMLGrid from the **upytl-standard** library and need not define any 
custom components.

The grid in action
..................

Lets now take a look at the controller for the grid which is very simple to see how it works.
::
    # apps/grid/controllers.py

    ...

    from .todo_db import db
    from .. common.common_utils import SimpleGrid

    ...
    
    @app.route('index')
    @app.use(gt.grid_template)
    def index(ctx: Context):
        db = ctx.db
        grid=SimpleGrid(ctx, 'db', db.todo, is_crud=False, page_title='Simple Grid no CRUD')
        
        if grid().accepted:
            ## do some additonal processing here
            print('Grid is good')
        else:
            ## raise the appropriate errors
            print('Grid is bad')
        return dict(grid= grid.get_options())        

Here we see that we intialise our grid passing in the arguments required. The most important thing to note
here is that we are telling our grid that is_crud is False. i.e we do not want this grid to have CRUD options

The 'db' could be any database that we have imported and the db.table could be any table in the db that we want to disply in 
grid form.

To see the **grid** app in action make sure that **Websaw** is running and in the browser head over to ``http://localhost.8000/grid``

.. note:: 
    You will probably need to populate your database with some date in order to see the results but we can
    always come back to that after our next **CRUD** section.

Now that we are able to present our data in **grid** format lets take a look at using **CRUD** next.