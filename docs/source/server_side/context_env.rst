Context environment
-------------------

Another import aspect of our **Context** is the ability to have a user defineable **local, configurable environment**.

This is extremely usefull when we want our actions to share common data and a typical use case for this would be 
using the environment to store the **menu** structure for an application which reflects the functionality of the application
and will generally only change when new actions are added or removed from the application.

The menus displayed to the user on the other hand will be based on the **role** of the user and as such will be different for each **role**

In order to avoid reading the menu structure from a data table or static file every time we need to display it, we simply include it in 
our **context environment** and have some logic to check roles etc.

Enivironment versus session
...........................

Both are used to share data between actions right?

The main difference btween **session** and **env** is that while **session** may not always be accesible by the **UI** layer eg: **templates**
the **context environment** has reserved a special key namely **default_template_context** specifically for this purpose.

**env** is also more secure and cannot be tampered with outside of the scope of the action.

Environment in action
.....................

So lets take a look at our **basic** app to see how this is used. In later examples we will see how to extend this to include 
**user role** to display the defined subset of menus depending on the **user role**. For now lets keep is simple.
::
    # apps/basic
    ...

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

    ...

Lets break this down. By now you shoul be familiar with **creating a custom fixture** which is what we are dong 
in this case a **GetUserMenu** fixture using the **Xauth** base fixture as it contains the majority of the hooks that our 
fixture requires.

.. note:: 

    We are intialting **navbar** from the **context** ctx. Navbar is a fixture that is part of the **auth** mixin so we 
    do not need to define our own for the basic app as we are using the **auth** mixin.

    **Current user** is a method of the **Xauth** fixture so we simply intialise it.

We then come to the part that we are most interested in here.
::
    ...
            ctx.env['default_template_context']['menu'] = [
                {'label': 'Home', 'href':ctx.URL('index')},
                {'label': 'About', 'href':ctx.URL('about')}
                ]
    ...

**default_template_context** is a **reserved** keyword in the **environment context** and is used specifically to make 
environment settings available to **templates**.

In the above example you can see that we are setting up our **menu** for our app.

As the **menu** fixture gets triggered on **take_on** this means that any action that uses this fixture will have the 
**menu** available when actioned.

Next lets take a look at the **Context** setup.
::
    ...

    class Context(info.Context, auth.Context, DefaultContext):
        env={
            'menus' : [],
            'menu': [],
            'default_template_context': dict(user = ''),
            'default_template_context': dict(buttons = ''),
            
        }
    ...
    
Here we declare our **env** and initilaise it with menus, menu and once again we set the **defualt_template_context** to some default
values or placeholders that our **app** will use in order to get the right information to our **template** or **templates**

Once again the majority of the processing is done in the **auth** mixin and our app simply intialises or changes the values to pass to the 
templates based on state of the application.

For example if a user is logged in we dont want to show them the login button on the menu. All this logic is taken care of by the 
**auth** mixin.

Simply by including this in our **action.use(...)** decorator as follows
::
    ...

    @app.route('index')
    @app.use(ctxd.menu, ctxd.index_template)  # note there is no session, but it used!
    def index(ctx: Context):

    ...

our **index** aciton will now be able to display the correct menu.

We can also override the **env** in our actitions as follows:
::
    ...

    ctx.env['default_template_context']['user'] = 'Fred'

    ...

A quick recap
.............

The **context environment** is generally used to pass information between **actions** in much the same way 
we could use our **session**

We can add anything we want to the **environment context** and access it from any acion using the **context**

We can update or change the values of our **local** environment inside our actions.

**default_template_context** is reserved for passing information to our **templates**