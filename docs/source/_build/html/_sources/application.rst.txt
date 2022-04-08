
.. _application:

===========
Application
===========

The **Application** layer is responsible for collecting routes along with mounting and wrapping each 
action by route handler with the correct setup/teardown procedures.

So far we have seen that we initialise the **Application** **(app)** using the DefaultApp app base class 
, provide the **app** with our desired **Context** and finally **mount** the **app**.

We have also seen how we can create custom **fixtures** that we can include in our custom **context** (**ctxd**)
which effectively make those fixture available to all **actions** using our **ctx**

So lets take a look at **routes** first of all.

A **route** indexes our **action** within the current **context** so calls to our **action** will be routed
correctly in all cases.

In order to simplify this and to avoid having to set up a seperate **routing table** we have the 
**@app.route()** decorator which allows us to define a route for a paticular action.
::
    
    @app.route('index')

effively sets up a route called 'index' inside our **app**.

The next convenience decorator we nned to look at is the **@app.use()** decorator.

This decorator is used to activate/decativate/teardown any **fixtures** we have created for 
our **index** action.

Most typically we would tell our app which form template to use by specifying the form name as follows:
::

    @action.use('index.html')

We could equally include any other fixture that we have created and add it to the list of **fixtures** that 
we want this particular action to use.

So if we go back to our **hello_world** example where we created a fixture to track the number of times 
someone visited out app we could equally as well add that fixture ONLY to our **index** action as follows:
::

    visited = Visited() ## our fixture 

    @app.route('index')
    @app.use('index.html', visited)
    def hello_world(ctx: Context)
        visited = visited.get_visits() ## note we are accessing our fixture directly
        return dict(msg='Hello Websaw World', visited=visited)

and in this case we would not need to include it in the **context**

.. note:: 

    Both the **index** and **visited** fixtures are initialised/loaded when the aciton is mounted and 
    similarly torn down when we leave the action.

This makes for super efficient actions and provides unlimited flexibility when designing and 
running our **app's actions**.

Now that we have coeverd the three layers or pillars that make up the *Websaw* framework stack lets 
take a look at what all this can do for us.

The first thing we are going to look at is the ability to **create** and **re-use** code forllowing 
the **DRY** coding pracitces. 

**DRY** or **Dont Repeat Yourself** coding is extremely important when developing larger and more complex
applications. 

Traditional web frameworks have generally involved a lot of code duplication whether or not it is html forms or 
similar actions used in multiple contollers.

**Websaw** overcomes this problem with the use of **MIXINS**

To find our more about **mixins** lets head over the :ref:`mixins` section right now.
