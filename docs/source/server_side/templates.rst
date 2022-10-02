
Component based Templating
--------------------------

Whilst most comparable frameworks make use of templates and rendering engines in order to generate html/css
in the required format for the client browser, **Websaw takes this one step furhter**

The ability to create **re-usable** components for use in our templates is a **huge benefit** both in terms of *RAD* as well
as providing consistancy and stability in **Websaw** apps.

A classic example would be a **search box** component which all applications requiring search functionality can include in 
any template to immediately have *search* functionality.

In order to achieve this **Websaw** utilises **UPYTL** for template rendering and ships with a **standard** component
library which will will cover in later sections.

So why UPYTL?
.............

**UPYTL** is an acronym for **Utlimate Python Templating Language** and as the name suggests it allows us to build our templates
in a *pythonic* way and takes much of its inspiration from **Vue.js**. 

In much the same way that **Vue** leverages the use of reusable embedded components for client side processing, **WebSaw**
leverages the use of similar embedded *re-usable* components for client/server applications.

Components can include other components and aslo include fucncionality at component level.

It is very simple to create a **library** of *custom componenets* that can be used in any prject simply by  importing the compnents that 
you intend to use for that particular project. Once againg the **DRY** coding practice is the driving force behind **UPYTL**
and as such we find it an excellent tool in our **Websaw** toolkit. 

Before we take a look at the **standard** components library that ships with **Websaw** lets take a look at building 
a few simple components of our own.

Anatomy of a component
......................

A **component** can be virtually anything from a **menu** to a **navbar** to a **field type** for a **form** and on and on.

The important thing to understand is that **components** can be made up of **other** components.

A classic use case for the above would be a standard **Form** component that consists of a variable number of **Field** componenets as well as 
**button** components based on the type of form we wish to generate.

.. important::
    
        **Components** take their input via **props** which can be thought of as the python equivalent of passing **args** to a function.

        **Components** interact with the application via **Slots**

        **Components** are stylable at component as such style attributes can be passed in as **props** to generate multiple variants of the 
        same component

        **Components** allow processing such as *For*, *If*, *Else* at component level.

        **Components** are grouped or used by **Templates** either singularly or collectively

        **Components** are extremely flexible


All this will become more apparent when we take a look at some of the **standard** componenets that ship with **Websaw**

For now lets start by taking a look at a simple **template** which will give us a good understanding of how **UPYTL**
works. As we move on we will see how we can easliy add **components** to our template.

The basic template
.................. 

As we are going to be looking at **Using mixins** in the next section lets start off by taking a look at the **info** mixin
that ships with **Websaw**. You can find the code at ``apps/mixins/info`` and we will start off by taking a look at the ``utemplates.py`` file.
::
    # apps/mixins/info/utemplates.py
    
    from upytl import html as h 

    # flake8: noqa E226

    welcome =  {
        h.Html():{
            h.Head():{
                h.Title():"[[app_get('app_name')]]",
                    h.Meta(charset='utf-8'):'',
                    h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css'):None, 
                },
                h.Body():{
                    h.Div(Class='box'):{
                        h.Div(Class='title is-5'):'This is the INFO MIXIN template',
                        h.Div(Class='title is-6'):'[[msg]]',
                    }
                },    
                h.Footer():{
                    h.Div(): 'This is the footer',
                }
            }
        }

As our **info mixin** does not require any fancy processing for now lets take a look at the above and break it down.

The first thing to note is that the template follows a very similar layout to any standard html template wiht 
**head**, **body** and **footer** sections. All of these could be components but for now lets keep is simple.

The second thing to note is just how **clean** the code is compared to a standard **HTML** template.

The key part on the template is the ``'[[msg]]'`` directive which is the input from the app.

.. note:: 
    
    We are using **Bulma** as our styling library of choice but any styling library such as **bootstrap**, **no.css** or 
    any library of your choice can be used and classes changed to refelct your choice.


Adding components
.................

As previously mentioned the main **benefit** of using components is the **re usablity** of our components in order to 
develop secure and robust applications rapidly with the minimum repetition.

To that end lets take a look at the **basic** application that ships with **Websaw** in order to demonstrate the 
basic usage of **mixins** and in particular the utemplates.py module and break it down.

Here we will be introducing the incorporation of **standard** components as well as using **custom** or *user-defined** components
that are used together in this particular example.
::
    # apps/basic/utemplates.py
    
    from upytl import SlotTemplate, html as h 

    from upytl_standard import HTMLPage, StandardNavBar 
    from ..common.common_components import Flash
    # flake8: noqa E226

    index = {
        HTMLPage(footer_class='custom-footer'):{
            SlotTemplate(Slot='nav'):{
                StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
            },
            SlotTemplate(Slot='flash'):{},
            
            SlotTemplate(Slot='content'):{
                h.Div(Class='box'):{
                    h.Div(Class='title is-4'): 'Welcome [[user]] from the default_template_context',
                    h.Div(Class='title is-5'): 'This is the mixin index Template. Select About to see more',
                    h.Div(For='f in msg'):{
                        h.Text():'[[ f ]] : [[msg[f] ]]',
                    }
                }    
            }
        }
    }

The first thing to note is that we introducing **SlotTemplate** by importing it form upytl.

As mentioned previously **Slots** are the main means that a components interact with the application.

**SlotTemplate** allows us to reference **Slots** defined in the master component .. in this case **HTMLPage** which 
is part of the **standard** componenets library.

To make this clearer lets take a look at the **HTMLPage** componenet as per the **standard** library.
::
    
    class HTMLPage(Component):
        props = dict(
            footer_class='page-footer',
            page_title="This is the page_title placeholder",
            nav = "This is our navbar placeholder"
        )
        template = {
            h.Html(): {
                h.Head():{
                    h.Title(): '[[page_title]]',
                    h.Meta(charset=b'utf-8'):'',
                    },
                h.Body():{
                    h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css'):None, 
                    h.Link(rel="stylesheet", href="https://cdn.datatables.net/1.10.24/css/jquery.dataTables.min.css"):None,
                    h.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css", integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==", crossorigin="anonymous"):None,
                    h.Script(src="https://code.jquery.com/jquery-3.5.1.js"):None,
                    h.Script(src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"):None,
                        
                    Slot(SlotName=b'nav'):{
                        h.Div():'No NavBar passed to the form'
                    },
                    Slot(SlotName=b'flash'):{
                        h.Div():'No Flash Message passed to the form'
                    },
                    Slot(SlotName=b'content'):{h.Div(): '[there is no default content]'},
                    Slot(SlotName=b'footer'):{
                        h.Footer(Class="footer is-small"):{
                            h.Div(Class= "content has-text-centered"):{
                                h.Template():{
                                    h.P(): 'Powered by UPYTL Standard Components (c) 2022',
                                }    
                            }
                        }
                    }
                }
            }
        }

While we will not get into this in too much detail for now the things to note are that apart teh **HTMLPage**
component declares a number of **Slots** that we will effectively link to in our template using **SlotTemplate**.

So ``Slot(SlotName=b'nav'):{...}`` will be overwritten by the actural contents of ``SlotTemplate(Slot='nav'):{...}``
in simple terms.

We will be covering a lot more examples of **templates** and **components** as we move through the guide but for now 
lets get back to our **mixins*

The main thing to note for now is that our **info** mixin has a template called **welcome** and our main app **basic** has a number
of templates which use **components** so lets take a look at how they interact in the next **Using mixins** seciton.



                    