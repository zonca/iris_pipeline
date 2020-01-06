***************************
Getting started
***************************

Requirements
============

First we need to install the requirements of the ``jwst`` package,
see `the JWST instructions
<https://github.com/spacetelescope/jwst/>`_,
reported here for convenience::

    conda create -n jwst_dev python=3.6 astropy
    source activate jwst_dev

then we need to install the ``jwst`` package, currently ``iris_pipeline``
is being tested with ``jwst`` 0.13.7::

    pip install https://github.com/spacetelescope/jwst/archive/0.13.7.zip

Then you need to download the ``CRDS`` cache:

.. code-block:: bash

    git clone https://github.com/oirlab/tmt-crds-cache $HOME/crds_cache

the ``CRDS`` cache contains metadata for IRIS, the calibration files, flat fields,
and a set of rules_ on how to choose the right calibration file given a set of metadata,
you can browse the content on `Github <https://github.com/oirlab/tmt-crds-cache>`_.

.. _rules: https://github.com/oirlab/tmt-crds-cache/blob/master/mappings/tmt/tmt_iris_flat_0001.rmap

Finally, we need a custom version of the ``CRDS`` library that contains some modules specific to TMT::

    git clone https://github.com/oirlab/tmt-crds.git
    cd tmt-crds
    pip install .

Development install
===================

First fork the repository under your account on Github,
then clone your fork on your machine.

Then enter the root folder and create a development install
with::

  pip install -e .
  
The development install doesn't add the ``tmtrun`` script to the path,
so you should do that manually::

  export PATH=$(pwd)/scripts/:$PATH

or symlink the ``tmtrun`` script from the conda environment `bin/` folder.
