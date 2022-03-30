.. _develop_label:


====================
Developing Your Apps
====================

In order to start developing your Websaw applications there are a number of things to do in order to set up your dev environment.

Fortunately there are a number of Websaw CLI options that automate and simplify this process of us.

If you are not familiar with the Websaw CLI please head over to the `Websaw CLI` section to familiarise yourelf with the options available.

To get started lets assume that we have no apps or app structure in our new Websaw development environment.

The quickest way to get started is to run the following:
::

    python -m websaw setup apps ## assuming apps is yoru root folder

This will create the apps folder for you in your working directory.

We can then install a dummy (scaffold) app by
::

    python -m websaw new_app -s <path to scaffold app zipfie>

Answer yes to the prompt and Websaw will install the scaffold app in the apps directory for you.

To test this fire up Websaw::

    python -m websaw run

open your browser and assuming the defaults::

    http://localhost/scaffold

should take you to the landing page of the recently installed scaffold app

CONGRATULATIONS!!


