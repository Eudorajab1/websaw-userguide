============
Introduction
============

**Websaw** (Web */Software Application Warehouse/*) is a lightweight, ultrafast web application framework
that offers feature rich **'out of the box functionality'** coupled with an unparalleled level of 
`flexibility` to develop *secure, robust applications* **rapidly**.

Main Features
*****************

    **Lightweight**
   
    * usese ombott a lightweight transport layer
    * small footprint
    * very few dependancies

    **Ultrafast**

    * modules and acrions load only the fixtures they use
    * no overhead on screen refresh or redirects
    * built on top of lighweight ombott transport layer

    **Feature rich**

    * standard authorization functionality
    * customizable default layout and page rendering 
    * customizable form templating engine
    * fully functional built in grid
    * customizable layout and .css libraries

    **Flexible**

    * create SPA or client server apps
    * incorporate js, vue or jquery components
    * connect seamlessly to multiple industry standard database engines

.. _design_overview:

Design Overview
**********************

**Websaw** has been designed to enable users of all levels to develop fully functional rich applicacaions 
irrespective of skill level or experience. In fact only a minimal knowledge of web developement is required to
get up and running in minutes.

**Websaw** consists of three distinct layers or pillars on which the entire framework stands:
    - **Fixtures**
    - **Context**
    - **Application**

**Fixtures** are *Websaw's* basic building blocks.
They can act as middleware (e.g. auth barrier or render routing action results using template)
**OR** as services (e.g. provide database connections) or a combination of the two.

**Context** is the *central hub* which is in charge of **fixture** maintenance (initialization/teardown/cleanup) 
as well as maintinaing communication between **actions** and **fixtures**. In addition the **comtext** layer
maintains communication between individual **fixtures** themselves.

.. note:: 

    In broad terms we can think of the **context** layer as the *services provider* and **fixtures** 
    as `services`.

The **Application** layer is responsible for collecting routes along with mounting and wrapping each action by 
route handler with the correct setup/teardown procedures.

All in all *Websaw* is truly a remarkably robust and flexible framework on which you can build amazing apps.

*Cant Wait to get started ?*

Head on over to :ref:`installation_label` section to get up and running in minutes
