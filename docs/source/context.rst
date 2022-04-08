
.. _context:

=======
Context
=======

As mentioned earlier **Context** (**ctx**) is the *central hub* which is in charge of **fixture** maintenance 
(initialization/teardown/cleanup) as well as maintinaing communication between **actions** and 
**fixtures**. 

In addition the **comtext** layer maintains communication between individual **fixtures** themselves.

Suffice to say the **context** layer is key to the *Websaw* framework and performs many 'under the hood'
functions in order to tie all layers together.

It is beyond the scope of this document to describe how the **context** layer functions in great 
detail as there is simply too much to cover here.

The main things to understand about the **context** layer are as follows:

* there are two builtin base classes of **context** namely **DefaultContxt** and **BaseContext**

* **ctxd** (design context) is how we refer to our context at module level 
  and generally override **DefaultContext**

* **cctx()** (current context) returns the context (ctx) from any context class

* **ctx** is always the first paramater in and action's function

To get the **ctx** using **cctx** you would do somthing like the following:
::
    
    ctx = BaseContext.cctx() OR
    ctx = DefaultContext.cctx()

Both are equivalent in this case.

We will see in later sections we we look at mixins and various other functionality just how much of an important 
role our **context** layer performs.

For now that is all we really need to know about **Context** so lets take a closer look at the 
:ref:`application` layer.  

    


