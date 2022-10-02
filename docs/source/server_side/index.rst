Server Side Applications
========================

Server Side or **Traditional** web applications have been around for a while now and fundamentally leverage on 
an application server or servers (normally web servers) to process any requests from the client which are passed on to the 
*backend* application which does the bulk of the work including the rendering of the output or *response* to the client
which is then sent back to the requesting browser via the web server/servers.

Applications that need to access large amounts of data and perform complicated processes based on user input 
or queries generally tend to employ this client/server approach for a whole host of reasons that are beyond the scope of 
this document, not least of which is a clear de-coupling of the UI (client) and data layers of the application.

While most **Traditional** python based web frameworks offer some form of re-usable code fucntionality at the application 
level, up until **Websaw** there has not been a reliable and easy way to create re-usable components that any or all applcations
can use/re-use in the way that some client side frameworks such as *Vue* are able to exploit.

This has generally meant a lot of code duplicaiton particularly at the UI layer for server side applications
which in turn leads to poor maintainablilty and difficultiy during enhancements and upgrades.

Whilst many frameworks claim to address these and some do address some of them **Websaw** has been developed 
specifically to address **ALL** the above and provide developers with a unique tool for **RAD** using **DRY** principles.

**WebSaw** provides the tools allowing developers to create sets of re-usable components both for response renedering as 
well as providing **mixin** functionality *out of the box* which allows us to develop applications/mixins that can be used 
by any or all others on the same domain.

Furthermore **WebSaw** allows logged in users to access multiple applications without having to logout and log in to each 
individual application as *standard* and *much much more*.

.. toctree::
    hidden

   getting_started
   fixtures
   context
   application
   templates
   mixins
   group_sessions
   context_env
   data_access
   simple_grid
   crud
