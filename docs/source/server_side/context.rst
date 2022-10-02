Application Context
-------------------

In order for our application to be functional we define and intialise our **Application Context**. This allows us to define
specific behaviour or charatersitics for each individual application based on our *Context* definition.

This is one of the most **powerfull** features of **Websaw** and as such we will be using it comprehensively as we build our apps.

What is meant by context?
.........................

**Context** is the *central hub* which is in charge of **fixture** maintenance (initialization/teardown/cleanup) 
as well as maintinaing communication between **actions** and **fixtures**. In addition the **comtext** layer
maintains communication between individual **fixtures** themselves.

The main things to understand about  **context** are as follows:
    * There are two builtin base classes of context namely DefaultContxt and BaseContext

        * ctxd (design context) is how we refer to our context at module level and generally override DefaultContext

        * cctx() (current context) returns the context (ctx) from any context class

        * ctx is always the first paramater in any action’s function

There is obviously a lot more to **conetxt** than the abouve and indeed it performs a lot of the *uner-the-hood* fucntionality that
we need not concern ourselves with.

We will see in later sections just how much of an important role the context layer plays in our applications.

Extending Context with our fixture
..................................

So lets extend the **DefaultContext** by including our **custom auth fixture** as follows:
::
    # apps/xauth/controllers.py

    # extend default context with our fixture
    class Context(DefaultContext):
        auth = auth

    ctxd = Context()

Thats it! Done.  We have extended our **context** with our **custom auth fixture**.

In later sections and in particular when we start looking at **mixins** we will expand upon this. 

For now we have our **auth** fixture in our **Context** and we are ready to move on.

.. important::
    
    At this stage we have  **ALL** default fixtures as per the DefaultContext **AS WELL AS** our custom fixture
    available to our appliation.

A quick recap
.............

So far we have :
    *   defined and intialised our **fixture**
    *   extended and intialised our **context**

The only thing left to do now is to intialise, mount and of course develop any applciation functionlaity that we need.

In order to do this we should look at our **Application** layer next where all of this takes place.

So lets get to it.
