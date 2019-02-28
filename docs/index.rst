***************************
iris_pipeline Documentation
***************************

The IRIS Data Reduction System is based on the ``stpipe`` package released by Space Telescope
for the James Webb Space Telescope.

With ``stpipe`` we can define a pipeline using JSON and CFG (text based .INI style files) and
custom analysis steps defined as classes in the current repository ``iris_pipeline``

Then execute the pipeline from the command line using the ``strun`` executable or using
directly the Python library.

The pipeline also dynamically interfaces to the ``CRDS`` the Calibration References Data System,
to retrieve the best calibration datasets given the metadata in the headers of the input FITS files.
The ``CRDS`` client can also load data from a local cache, so for now we do not have a actual
``CRDS`` server and we only rely on a local cache.

The ``CRDS`` is not under our control, the Thirty Meter Telescope will deliver a database system
to replace the ``CRDS`` and we can adapt our code to that in the future.

Getting Started
===============

.. toctree::
   :maxdepth: 2

   getting-started

Example run
===========

.. toctree::
   :maxdepth: 2

   example-run

Design
======

.. toctree::
   :maxdepth: 2

   design

Calibration
===========

.. toctree::
   :maxdepth: 2

   calibration-database

Algorithms
==========

.. toctree::
   :maxdepth: 1

   algorithms

Reference/API
=============

.. automodapi:: iris_pipeline
