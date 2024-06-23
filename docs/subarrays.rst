*********************
Support for subarrays
*********************

Support for subarrays is currently only implemented for the imager and it supports
datasets where only a custom subset of the 2D array is observed.

The keywords of :py:class:`IRISImageModel` which defines the parameters of the
subarray are::

    model.meta.subarray.name = "CUSTOM"
    model.meta.subarray.id = 1
    model.meta.subarray.xstart = xstart + 1
    model.meta.subarray.ystart = ystart + 1
    model.meta.subarray.xsize = xsize
    model.meta.subarray.ysize = ysize

Consider that following the FITS conventions the `xstart` and `ystart` keywords
are 1-based, therefore the default `xstart` is 1 and if you are slicing an
array in Python, you should add 1 to the keyword before saving it into the metadata.
`subarray.id` is saved into the FITS keyword `SUBARRID` and should be 0 for full
frames, 1 for the first subarray and so on.

The name of an entire frame is "FULL".

Subarrays and reference files
=============================

Flat frames, darks and background files either in CRDS or using local overrides
can either be saved as subarrays
or can be saved as full frames. In case they are saved as full frames, after being
accessed they are sliced according to the metadata in the input subarray.

Example usage
=============

As usage examples, check the notebooks or the ``test_image2.py`` script in the
`unit tests folder in the repository <https://github.com/oirlab/liger_iris_pipeline/tree/master/liger_iris_pipeline/tests>`_

Related steps
=============

.. toctree::
   :maxdepth: 2

   parse_subarray_map/index.rst
   merge_subarrays/index.rst
