Example pipeline execution
==========================

Here is an example of what it takes to configure and run a pipeline with
flat-fielding and background subtraction, 

Setup CRDS
----------

Make sure you have a local checkout of the CRDS cache as explained in the 
`Getting started <getting-started>`__ page.
Run the ``setup_local_crds.sh`` to setup the enviroment variables needed
to point the ``crds`` software to the CRDS cache. Optionally source
this in your shell configuration to automatically set this up.

Get input simulations
---------------------

Download simulated input FITS files for the IRIS
imager from `Figshare <https://figshare.com/articles/TMT_IRIS_test_simulations/9941939>`_.
It contains a raw science frame, a raw flat frame and a raw background frame.

Preprocess the flat frame
-------------------------

First we need to remove the dark frame from the flat frame and normalize it.
A dark frame is already available in the CRDS and the pipeline knows how to retrieve
it based on the metadata in the FITS file headers.

We can check in the package `documentation <https://iris-pipeline.readthedocs.io/en/latest/#module-iris_pipeline>` what are the available pipelines and check the configuration options of the :py:class:`pipeline.PreprocessFlatfield` class.

We do not need to customize it so we can directly call it from ``tmtrun`` and pass the input FITS file::

    tmtrun iris_pipeline.pipeline.PreprocessFlatfield raw_flat_frame_cal.fits

This will pickup the relevant dark frame from the CRDS and process the file:

.. code:: bash

    2019-10-04 17:59:48,057 - stpipe.PreprocessFlatfield - INFO - PreprocessFlatfield instance created.
    2019-10-04 17:59:48,059 - stpipe.PreprocessFlatfield.dark_current - INFO - DarkCurrentStep instance created.
    2019-10-04 17:59:48,060 - stpipe.PreprocessFlatfield.normalize - INFO - NormalizeStep instance created.
    2019-10-04 17:59:48,099 - stpipe.PreprocessFlatfield - INFO - Step PreprocessFlatfield running with args ('raw_flat_frame_cal.fits',).
    2019-10-04 17:59:48,554 - stpipe.PreprocessFlatfield - INFO - Prefetching reference files for dataset: 'raw_flat_frame_cal.fits' reftypes = ['dark']                                                                                                                      
    2019-10-04 17:59:49,306 - stpipe.PreprocessFlatfield - INFO - Prefetch for DARK reference file is '/home/azonca/crds_cache/references/tmt/iris/tmt_iris_dark_0001.fits'.                                                                                                  
    2019-10-04 17:59:49,307 - stpipe.PreprocessFlatfield - INFO - Starting preprocess flatfield ...
    2019-10-04 17:59:53,490 - stpipe.PreprocessFlatfield - INFO - Processing product raw_flat_frame
    2019-10-04 17:59:53,490 - stpipe.PreprocessFlatfield - INFO - Working on input raw_flat_frame_cal.fits ...
    2019-10-04 17:59:53,641 - stpipe.PreprocessFlatfield.dark_current - INFO - Step dark_current running with args (<IRISImageModel(4096, 4096) from raw_flat_frame_cal.fits>,).
    2019-10-04 17:59:53,658 - stpipe.PreprocessFlatfield.dark_current - INFO - Using DARK reference file /home/azonca/crds_cache/references/tmt/iris/tmt_iris_dark_0001.fits
    2019-10-04 17:59:54,058 - stpipe.PreprocessFlatfield.dark_current - INFO - Step dark_current done
    2019-10-04 17:59:54,101 - stpipe.PreprocessFlatfield.normalize - INFO - Step normalize running with args (<IRISImageModel(4096, 4096) from raw_flat_frame_cal.fits>,).
    2019-10-04 17:59:54,472 - stpipe.PreprocessFlatfield.normalize - INFO - Step normalize done
    2019-10-04 17:59:54,472 - stpipe.PreprocessFlatfield - INFO - Finished processing product raw_flat_frame
    2019-10-04 17:59:54,473 - stpipe.PreprocessFlatfield - INFO - ... ending preprocess flatfield
    2019-10-04 17:59:54,811 - stpipe.PreprocessFlatfield - INFO - Saved model in raw_flat_frame_flat.fits
    2019-10-04 17:59:54,811 - stpipe.PreprocessFlatfield - INFO - Step PreprocessFlatfield done

We have an output file ``raw_flat_frame_flat.fits`` and we can rename it::

    mv raw_flat_frame_flat.fits flat.fits

Configure the image processing pipeline
---------------------------------------

The :py:class:`Image2Pipeline` can be configured using a INI-style configuration file,
``image2_iris.cfg``:

.. code-block:: ini

   name = "Image2Pipeline"
   class = "iris_pipeline.pipeline.Image2Pipeline"
   save_results = True
       [steps]
         [[bkg_subtract]]
         [[assign_wcs]]
           skip = True
         [[flat_field]]
           config_file = flat_field.cfg
         [[photom]]
           skip = True
         [[resample]]
           skip = True

first we specify that we want to execute the pipeline defined in
:py:class:`iris_pipeline.pipeline.Image2Pipeline`, then we can configure each of
the steps, for example skip some of them. Also we can import the
configuration of a step from another file, in this case
``flat_field.cfg``:

.. code-block:: ini

   name = "flat_field" 
   class = "jwst.flatfield.FlatFieldStep"
   # Optional filename suffix for output flats (only for MOS data).
   flat_suffix = None
   override_flat = 'flat.fits'

If we do not define ``override_flat``, the pipeline will look up a suitable flat from
the CRDS, in this case instead we specify a local ``flat.fits`` file.

Define the input data
---------------------

JWST created a specification for defining how input files should be used
by a pipeline, it is a JSON file named an association, see `the JWST
documentation <https://jwst-docs.stsci.edu/display/JDAT/Understanding+Associations>`__.

In our example we need to specify a input raw science frame ad a
background to be subtracted, see ``asn_subtract_bg_flat.json``:

.. code:: json

   {
       "asn_rule": "Asn_Lv2Image",
       "asn_pool": "pool",
       "asn_type": "image2",
       "products": [
           {
               "name": "test_iris_subtract_bg_flat",
               "members": [
                   {
                       "expname": "raw_science_frame_sci.fits",
                       "exptype": "science"
                   },
                   {
                       "expname": "raw_background_frame_cal.fits",
                       "exptype": "background"
                   }
               ]
           }
       ]
   }

Execute the pipeline from the command line
------------------------------------------

We can use ``tmtrun`` from a terminal to execute the pipeline:

::

   tmtrun image2_iris.cfg asn_subtract_bg_flat.json

here is the output log:

.. code:: bash

    2019-10-04 18:13:46,453 - stpipe.Image2Pipeline - INFO - Image2Pipeline instance created.
    2019-10-04 18:13:46,454 - stpipe.Image2Pipeline.bkg_subtract - INFO - BackgroundStep instance created.
    2019-10-04 18:13:46,456 - stpipe.Image2Pipeline.assign_wcs - INFO - AssignWcsStep instance created.
    2019-10-04 18:13:46,458 - stpipe.Image2Pipeline.dark_current - INFO - DarkCurrentStep instance created.
    2019-10-04 18:13:46,460 - stpipe.Image2Pipeline.flat_field - INFO - FlatFieldStep instance created.
    2019-10-04 18:13:46,461 - stpipe.Image2Pipeline.photom - INFO - PhotomStep instance created.
    2019-10-04 18:13:46,463 - stpipe.Image2Pipeline.resample - INFO - ResampleStep instance created.
    2019-10-04 18:13:46,500 - stpipe.Image2Pipeline - INFO - Step Image2Pipeline running with args ('asn_subtract_bg_flat.json',).
    2019-10-04 18:13:47,130 - stpipe.Image2Pipeline - INFO - Prefetching reference files for dataset: 'raw_science_frame_sci.fits' reftypes = ['dark']
    2019-10-04 18:13:47,645 - stpipe.Image2Pipeline - INFO - Prefetch for DARK reference file is '/home/azonca/crds_cache/references/tmt/iris/tmt_iris_dark_0001.fits'.
    2019-10-04 18:13:47,645 - stpipe.Image2Pipeline - INFO - Override for FLAT reference file is '/home/azonca/p/software/iris_pipeline/iris_pipeline/tests/data/flat.fits'.
    2019-10-04 18:13:47,645 - stpipe.Image2Pipeline - INFO - Prefetching reference files for dataset: 'raw_background_frame_cal.fits' reftypes = ['dark']
    2019-10-04 18:13:47,651 - stpipe.Image2Pipeline - INFO - Prefetch for DARK reference file is '/home/azonca/crds_cache/references/tmt/iris/tmt_iris_dark_0001.fits'.
    2019-10-04 18:13:47,651 - stpipe.Image2Pipeline - INFO - Override for FLAT reference file is '/home/azonca/p/software/iris_pipeline/iris_pipeline/tests/data/flat.fits'.
    2019-10-04 18:13:47,651 - stpipe.Image2Pipeline - INFO - Starting calwebb_image2 ...
    2019-10-04 18:13:47,659 - stpipe.Image2Pipeline - INFO - Processing product test_iris_subtract_bg_flat
    2019-10-04 18:13:47,659 - stpipe.Image2Pipeline - INFO - Working on input raw_science_frame_sci.fits ...
    2019-10-04 18:13:47,918 - stpipe.Image2Pipeline.bkg_subtract - INFO - Step bkg_subtract running with args (<IRISImageModel(4096, 4096) from raw_science_frame_sci.fits>, ['raw_background_frame_cal.fits']).
    2019-10-04 18:13:53,796 - stpipe.Image2Pipeline.bkg_subtract - INFO - Step bkg_subtract done
    2019-10-04 18:13:53,854 - stpipe.Image2Pipeline.assign_wcs - INFO - Step assign_wcs running with args (<IRISImageModel(4096, 4096) from raw_science_frame_sci.fits>,).
    2019-10-04 18:13:53,855 - stpipe.Image2Pipeline.assign_wcs - INFO - Step skipped.
    2019-10-04 18:13:53,856 - stpipe.Image2Pipeline.assign_wcs - INFO - Step assign_wcs done
    2019-10-04 18:13:53,898 - stpipe.Image2Pipeline.dark_current - INFO - Step dark_current running with args (<IRISImageModel(4096, 4096) from raw_science_frame_sci.fits>,).
    2019-10-04 18:13:53,945 - stpipe.Image2Pipeline.dark_current - INFO - Using DARK reference file /home/azonca/crds_cache/references/tmt/iris/tmt_iris_dark_0001.fits
    2019-10-04 18:13:54,503 - stpipe.Image2Pipeline.dark_current - INFO - Step dark_current done
    2019-10-04 18:13:54,566 - stpipe.Image2Pipeline.flat_field - INFO - Step flat_field running with args (<IRISImageModel(4096, 4096) from raw_science_frame_sci.fits>,).
    2019-10-04 18:13:55,328 - stpipe.Image2Pipeline.flat_field - INFO - Step flat_field done
    2019-10-04 18:13:55,369 - stpipe.Image2Pipeline.photom - INFO - Step photom running with args (<IRISImageModel(4096, 4096) from raw_science_frame_sci.fits>,).
    2019-10-04 18:13:55,369 - stpipe.Image2Pipeline.photom - INFO - Step skipped.
    2019-10-04 18:13:55,370 - stpipe.Image2Pipeline.photom - INFO - Step photom done
    2019-10-04 18:13:55,370 - stpipe.Image2Pipeline - INFO - Finished processing product test_iris_subtract_bg_flat
    2019-10-04 18:13:55,370 - stpipe.Image2Pipeline - INFO - ... ending calwebb_image2
    2019-10-04 18:13:55,606 - stpipe.Image2Pipeline - INFO - Saved model in test_iris_subtract_bg_flat_cal.fits
    2019-10-04 18:13:55,606 - stpipe.Image2Pipeline - INFO - Step Image2Pipeline done

After
completion, the reduced science frame
``test_iris_subtract_bg_flat_cal.fits`` is written to disk, it includes
all the metadata it had initially and additional details about the
processing steps that were executed.
