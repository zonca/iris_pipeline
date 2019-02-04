***************************
iris_pipeline Documentation
***************************

The IRIS Data Reduction System is based on the `stpipe` package released by Space Telescope
for the James Webb Space Telescope.

With `stpipe` we can define a pipeline using JSON and CFG (text based .INI style files) and
custom analysis steps defined as classes in the current repository `iris_pipeline`.

Then execute the pipeline from the command line using the `strun` executable or using
directly the Python library.

The pipeline also dynamically interfaces to the `CRDS`, the Calibration References Data System,
to retrieve the best calibration datasets given the metadata in the headers of the input FITS files.
The `CRDS` client can also load data from a local cache, so for now we do not have a actual
`CRDS` server and we only rely on a local cache.

The `CRDS` is not under our control, the Thirty Meter Telescope will deliver a database system
to replace the `CRDS` and we can adapt our code to that in the future.

Requirements
============

First we need to install the requirements of the ``jwst`` package,
see `the JWST instructions
<https://github.com/spacetelescope/jwst/#installing-the-latest-development-version>`_,
reported here for convenience::

    conda create -n jwst_dev --only-deps --override-channels -c http://ssb.stsci.edu/astroconda-dev -c defaults python=3.6 jwst
    source activate jwst_dev

then we need to install the ``jwst`` package, in the future we will be able to use
the package released by Space Telescope, for now I have some minor modifications,
therefore you need to install my fork::

    git clone --branch iris_devel https://github.com/zonca/jwst
    cd jwst
    python setup.py install

Then you need to download the ``CRDS`` cache::

    git clone https://github.com/oirlab/tmt-crds-cache $HOME/crds_cache

the ``CRDS`` cache contains metadata for IRIS, the calibration files, flat fields,
and a set of `rules on how to choose the right calibration file given a set of metadata<https://github.com/oirlab/tmt-crds-cache/blob/master/mappings/tmt/tmt_iris_flat_0001.rmap>`_,
you can browse `the content on Github<https://github.com/oirlab/tmt-crds-cache>`_.

Development install
===================

First fork the repository under your account on Github,
then clone your fork on your machine.

Then enter the root folder and create a development install
with::

  pip install -e .

Example pipeline
================

You can then run a example pipeline to subtract the background and apply flat-fielding
to a simple simulated observation of the imager::

    git clone https://github.com/oirlab/IRIS-data-reduction-tests
    cd IRIS-data-reduction-tests/201901_stpipe_iris_pipeline

then run the bash script ``run.sh``::

    bash run.sh

this will load the input files `sci.fits` and `bg.fits`, retrieve a flat from the ``CRDS`` cache
and then perform the pipeline steps defined in the configuration file and output a reduced frame
in FITS format.

Reference/API
=============

.. automodapi:: iris_pipeline
