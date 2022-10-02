Group sessions
--------------

Group sessions are available to all **Websaw** applications running on the same domain if required. 

Group sessions in essence allow a user to **log in** to any application on the domain that they have access to 
and immediatley have access to all other applications if so required.

So why use group sessions?
..........................

Group sessions are extremely convenient when developing larger applications which are split up into multiple applications.

A typical use case would be a **CRM** application consisiting of multiple applications each performing a specific set of tasks.

Users which have access to multiple **applications** would generally need to log in to each application at least once in order 
to have access to that application or use some sort of centralized authentication token determining access to individual apps.

With group session as described above a user needs to log in only once in order to have access to all the applictaions they are entitled
to.

Group sessions in action
........................ 

So lets take a look at how we set up a **group session** in **Websaw**.

As we saw in the **basic app**, we can easily declare a **group** for our **group session**

We do this as follows:
::
    ...
    ctxd = Context()
    app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)
    ...

The above is giving our **group session** the **group_name** of 'websaw_apps_group_one'. We could name this 
anything we like and only applications that **belong** to this **group_name** will grant access to users logged in to this
**group_name** session.

In practical terms and to follow on from our above *typical use case* let us say that we have a **group_name** of 'accounts' to which
belong all users that should be able to access any application that has anything to do with **accounting**

Any user that has access to this **group_name** will be able to access any application that supports **group_name = 'accounts'**
without having to log out and in again irrespective of which app they logged into first.

.. important:: 
    
    This is an extremely powerfull feature and care should be taken when assigning access rights in order to ensure
    that only authorised users access the correct applications.

    
