IRIS Data Reduction System design
=================================

Introduction
============

The IRIS Data Reduction System is planned to perform:

-  real-time (< 1 minute) and offline data processing of IRIS images and
   spectroscopic data with the
   :py:mod:`iris_pipeline` Python
   package based on JWST’s pipeline package
   ``stpipe``, see `the documentation <https://jwst-pipeline.readthedocs.io/en/latest/jwst/stpipe/>`_
-  raw readout processing from the IRIS imager and spectrograph into raw
   science quality frames with the C library
   ``iris_readout`` at https://github.com/oirlab/iris_readout, which
   will be used directly during real-time operations and will be wrapped
   into Python modules in ``iris_pipeline`` for offline processing.
-  visualization of raw and reduced data to facilitate data assessment
   and analysis for real-time and offline use. These tools will be
   developed later and will possibly be based on existing community
   software tools like `DS9 <http://ds9.si.edu/site/Home.html>`_ or
   `cubeviz <https://cubeviz.readthedocs.io/>`_.

Software infrastructure
=======================

We rely on the excellent work mostly by Space Telescope to grow the
Python in Astronomy ecosystem around the ``astropy`` package. They also
developed a suite of open-source tools to operate JWST based on their
experience operating the Hubble Space telescope.

The :py:mod:`jwst` Python package
bundles several tools:

-  a :py:mod:`jwst.datamodel` package to handle custom schemas for complex
   hierarchical metadata
-  a :py:mod:`stpipe` package to configure and execute processing pipelines
-  a large array of data processing modules to analyze data from all
   instruments on board of JWST

We leverage this effort by:

-  building a custom schema for IRIS
-  using ``stpipe`` to execute our pipelines
-  starting from JWST processing modules and customizing them for IRIS
   and publishing them on the ``iris_pipeline``
   repository https://github.com/oirlab/iris_pipeline.

Example run
===========

The best way to understand how ``iris_pipeline`` works is to checkout an
`example reduction <example-run>`_ of a raw science frame to a reduced
science frame with flat-fielding and background subtraction.

Access calibration files via the Calibration Reference Data System (CRDS)
=========================================================================

The `Calibration Reference Data System
(CRDS) <https://hst-crds.stsci.edu/static/users_guide/overview.html>`_
is a set of tools developed by Space Telescope to organize and retrieve
calibration reference files, e.g. flat frames, dark frames, for JWST and
HST. When ``stpipe`` is executing a pipeline, it can automatically
connect to the JWST CRDS server and get the right flat based on the
metadata in the header of the data FITS files. The logic necessary to
choose the right file is encoded in text files. Those configuration
files and the actual calibration FITS files are also cached locally so
that the CRDS client library works even without any connection to a
central server.

We have created a CRDS cache folder in the Github repository
https://github.com/oirlab/tmt-crds-cache,
this includes in the ``mappings/tmt``
`folder <https://github.com/oirlab/tmt-crds-cache/tree/master/mappings/tmt>`_
the metadata for IRIS and the rules to choose the right flat-field
frame, for now there is only a dummy rule but this can be easily
customize querying the metadata in the input file.

Currently we do not have any CRDS server running, but the users can
download the CRDS cache locally and use it anyway, see the `Getting
started <getting-started>`_ documentation.

Also, the CRDS client library needs to have minimal knowledge about
metadata for TMT, therefore we maintain a fork of that library which
simply adds a submodule dedicated to IRIS, https://github.com/oirlab/tmt-crds, it is quite
easy to upgrade this to newer releases of CRDS by Space Telescope.

If TMT decided to use CRDS as their Data Management System, it would
leverage the extensive set of tools and documentation available and
would not require modifications to ``stpipe``; otherwise, we will
implement support for the DMS API into (our own fork of) ``stpipe``.
