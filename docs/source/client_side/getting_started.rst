SPA Getting Started
===================

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
--------------------------

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
