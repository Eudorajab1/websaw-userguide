Client Side Applications
========================

Client Side Application or **SPA** development essentially involves using a client side programming language such as 
**Javascript** or one of the many derivatives thereof in order to develop applications that essentially render and run in the client browser
as opposed to **Traditional** web apps where the bulk of the processing is done on the application server.

There are many instances where this form of applicaion is preferrable to the **Traditioanl** way of processing 
and typically developers will decide on the type of application they will develop based on functional requirements.

How and when or why to use **SPA** as opposed to **Traditional** technology is beyond the scope of this document and 
we assume that you are at least familiar with the pros and cons of using each type of application.

For now let us focus on how **WebSaw** allows the development of **SPA** by examining **PyJsaw**.

**PyJsaw** is an acronym for **Python Javascript Application Warehouse** which much like **Websaw** itself offers us the means
to develop our **SPA** quickly and securely usng structured pythonic code and leverages on providing a **RapydScript** structure
for generating **Vue** componenets.

However complex our application requirement the end result will always be an application that has a single
entry point (traditionally 'index') which will pass processing back control to our **SPA**.

All futher processing/rendering is then performed by our **SPA** client side.

Whilst there is nothing preventing us from coding our **SPA** in **Vue.js** directly or even vanilla .JS we will see how **PyJsaw** will simplify 
this whole process for us and give us the ablilty to create stunning **SPA** apps quicky and sercurely.

.. toctree::

   getting_started
   scaffold_app
   
