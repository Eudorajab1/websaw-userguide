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