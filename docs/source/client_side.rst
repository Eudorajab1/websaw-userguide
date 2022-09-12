.. _client_side:

========================
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

SSA Getting Started
-------------------

If you have followed the :ref:`installation_label` installation procedures as outlined in the :ref:`getting_started` section
you should already have **PyJsaw** installed.

In order to test this simply open up your browser or click on http://localhost:8000/pyjsaw

If all is good you will see a login screen prompting you for the admin password. This is the password that you set up during the 
initial installation.

Once the correct password has been entered you will see the **PyJsaw** IDE screen and we are ready to go.

If you are unable to login the most common cause is that you have not set up your admin password via the **WebSaw** cli.
We strongly reccomend you take a look at the following depending on your choice of installation method and 
repeat the :ref:`installation_label` or initialise the admin password.  

.. important::

    The **vuepy** folder in our spa_hello app is essentially our **SPA** working folder and it is here
    that we will develop our application.

Before we jump into our **SPA** development it is important to understand the makeup of our **VuePy** files.

Understanding PyJsaw files
..........................

PyJsaw files can consist of several specific parts (all of which are optional):
::
    # vuepy/foo.vuepy

    #This is the RapydML-like part - will be compiled to views/foo.html
    html:
        head:
        ...
        body:
            div(id = 'app'):
        script(src = "{{=URL('static', 'js/foo.js')}}"):
        
    # This is the vue template part - will be compiled to html string 
    # and injected into the v-pyj part as the foo_templ variable (see below)    
    v-def foo_templ:
    div:
        vtitle(title = '...'):
        ul:
            li(v-for = 'it in items'): '{{it}}'
    ...
    
    # This is v-pyj part (regular rapydscript) - will be compiled to static/js/foo.js    
    v-pyj:
        # template will be injected here as variable:
        #foo_templ = '''
        #<div>
        #    <vtitle title = '...'></vtitle>
        #    <ul>
        #       ...
        #    </ul>
        #</div>
        #'''
        
        # it's also possible to import title.vuepy (if we have one) as regular pyj file!
        # it will be compiled to pyj on-the-fly and returned to the rapydscript compiler  
        import title # - Note, that we just import title.vuepy, title.html/js files will not be created     
        vopt = {
            template: foo_templ, 
            delimiters:['{{','}}'],
            data:{items[...]},
            el:'#app',
            components:{'vtitle': title.vopt}
        }
        def main():
            app = new Vue(vopt)
        if __name__=='__main__':
            main()

The SPA Scaffold Application
............................

WebSaw ships with a standard spa_scaffold app that can be used as a template for developing **SPA** apps. 

The code is pretty much self explanatory and we suggest to take a look at each of the modules in the spa_scaffold app and familiarise yourself with 
how it all hangs together. We will however focus on a few specific modules in a bit more detail.

In order to have a point of reference as we walk through the code it is advisable to open your browser and 
head over to http://localhost:8000/spa_scaffold where you will see the scaffold app.

In essense any **SPA** application will generally consist of one or more *pages* and one or more *components*. The scaffold app
groups these together in two main folders nameley *bundled_pages* and *bundled_componenets*. Thes will in turn be combined in our *spa_bundle* which will invarialbly consist
of all pages and components we intent to use in our app.

So lets start off by taking a look at a typical page.
::
    # vuepy/spa/pages/page_one.vuepy
    # Don't forget to Compile me!
    v-def templ:
        layout:
            p: 'This page stored in static/spa/pages/page_one.js'
            p: 'It was created using pyjsaw, src: vuepy/spa/pages/page_one.vuepy'
            p: 'After changes vuepy-file just press `Compile` to update js-file'
            button(@click='count+=1'): 'Click me'
            div: 'count: {{count}}'

    v-pyj:
        pg = {
            template: templ,
            def data(self):
                return {count: 1}
        }

        define([], def(): return pg;)

This is a simple page that is basically recording the number of times a user clicks on the button. You will see
that we have both a *templ* section as well as a *v-pyj* section to our *vuepyj* file. The rest should be pretty much
self explanatory.

.. note::
    It is important to compile this file any time you make any changes to either of the sections.

Now lets take a look at a slightly different page as follows:
::
    # Don't forget to Compile me!
    layout:
        p: 'This is demo of what you can do using only vue-template, without js.'
        div:
            input(v-model='search_input'):
            button(@click='redirect({search:search_input})', :disabled='!search_input'):
                'Search'
            button(@click='(search_input="", redirect())'):
                'Reset'
        div:'Seacrh result:'
        div(v-if='search_result'):
            '{{search_result}}'
        div(v-else-if='search_input && search_input == last_search_input'):
            'Nothing was found'
        div(v-else):
            'Try to search'
 
As you can see we do not need to include all sections of the vuepy file in order to user it effectively.

As our page is effectively using the *search_box* component lets take a look at this component and see how we can create
components in a *pythonic way*
::
    # Don't compile me
    # import me in vuepy/bundled_pages/__init__.pyj
    # and recompile vuepy/spa_bundle.pyj after changes
    v-def templ:
        span:
            input(v-model='input_search', :disabled='is_loading'):
            button(@click='$emit("input_search", input_search)', :disabled='is_loading'):
                '{{button_text}}'

    v-pyj:
    @{

    async import spa_tools

    vc = spa_tools.v_collector()

    @vc.component()
    class Component(spa_tools.RSVue):
        def __init__(self):
            self.name = __name__
            self.template = templ
            self.props = ['current_search', 'is_loading']

        def data(self):
            return {
                input_search: self.current_search,
                button_text: 'Search',
            }

        @vc.watch('current_search')
        def watch_current_search(self, n, o):
            self.input_search = n

        @vc.watch('is_loading')
        def watch_is_loading(self, n, o):
            self.button_text = n ? 'Loading...' : 'Search'


    def make():
        return Component()

    }@

From the above you can see that we create our *Component* class with the methods we want our componet to use.

This is done by using decorators based on the standad vue functionality we want to use and follows the same naming conventions.

Our component will always be a subclass of *spa_tools.RSVue* allowing **PyJsaw** to create the relevant .js code
based on the @vc.<> decorator. In this case we are leveraging the vue watch fucntionality to detect any changes to our search component.

Please take some time to go through the rest of the spa_scaffold application and start developing your own **SPA** applications
using the spa_scaffold app as your template.

Next Steps
..........

Full working examples of **SPA** complete applications can be found on the `Websaw Workshop <https://websaw-workshop.readthedocs.io/en/latest/getting_started.html>`_ site along with 
code. Feel free to visit soon.