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

See `the section about Calibration <calibration-database>`_

Metadata
========

`iris_pipeline` requires a set of metadata from TMT and from other subsystems to process the data,
see the `list of required metadata <https://github.com/tmt-icd/IRIS-Model-Files/blob/master/drs/drs-assembly/subscribe-model.conf>`_.

Moreover, `iris_pipeline` will add to the header of processed FITS files categorizing the data in:

===================  ==================================  ======================================
OBSTYPE              OBSNAME                             Description
===================  ==================================  ======================================
Calibration (CAL)    IMG1-NFF, SLI-NFF                   Flat field
                     LEN-SPX                             Lenslet Spectral Extraction
                     IMG1-DRK, SLI-DRK, LEN-DRK          Master dark
                     IMG1-TEL, SLI-TEL, LEN-TEL          Telluric Star
Engineering (ENG)    SLI-IDP, LEN-IDP                    Instrumental dispersion
Science (SCI)        IMG1-SCI, LEN-SCI, SLI-SCI          Science
                     IMG1-SKY, LEN-SKY, SLI-SKY          Sky
===================  ==================================  ======================================
