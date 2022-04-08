
.. _mixins:

======
Mixins
======

    **Mixins have to be one of the most innovative and time saving features of Websaw**

So what exactly is a mixin?
--------------------------

In essence a **mixin** can be anything that you could use in any other application. 

This can range from a simple generic action (such as a logger) to an application itself.

In order to understand **mixins** lets take a look at the **simple** application that ships as 
standard with *Websaw* and see how it all fits together.

The first thing that we need to note is that by convention in our apps directory structure we have a
folder called **mixins** and yes you guessed it .. this is where we store our **mixins**.

The only real difference between **mixins** and **apps** is that we do not mount our mixins. 

Instead the *host* application will mount the **mixin** or even multiple **mixins** as part of its 
own **mount()**.

All **mixin** functionality including templates, actions fixtures and databases as created in the 
**mixin** is immediately available to the **host** app.

So lets take a look at an example:








