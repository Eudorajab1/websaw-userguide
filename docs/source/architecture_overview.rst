.. _arch_overview:

Architecture Overview
**********************

**Websaw** has been designed to enable users of all levels to develop fully functional rich applicacaions 
irrespective of skill level or experience. In fact only a minimal knowledge of web developement is required to
get up and running in minutes.

**Websaw** consists of three distinct layers or pillars on which the entire framework stands:
    - :ref:`Fixtures`
    - :ref:`Context`
    - :ref:`Application`

WebSaw Fixtures:
----------------

**Fixtures** are *Websaw's* basic building blocks.
They can act as middleware (e.g. auth barrier or render routing action results using template)
**OR** as services (e.g. provide database connections) or a combination of the two.

To learn more about **WebSaw** fixtures you can head over to the :ref:`fixtures` section.

The Context Layer:
------------------


**Context** is the *central hub* which is in charge of **fixture** maintenance (initialization/teardown/cleanup) 
as well as maintinaing communication between **actions** and **fixtures**. In addition the **comtext** layer
maintains communication between individual **fixtures** themselves.

To learn more about the **Context** layer you can head over to the :ref:`context` section.

.. note:: 

    In broad terms we can think of the **context** layer as the *services provider* and **fixtures** 
    as `services`.

The Application Layer:
----------------------

The **Application** layer is responsible for collecting routes along with mounting and wrapping each action by 
route handler with the correct setup/teardown procedures.

To learn more about the **Application** layer you can head over to the :ref:`application` section.

All three layers intergrate seamlessly to provide the ultimate in web application frameworks.
