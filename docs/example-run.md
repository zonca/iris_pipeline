Example pipeline execution
==========================

Here is an example of what it takes to configure and run a pipeline with flat-fielding and background subtraction,

## Create configuration files

First we configure our pipeline using a INI-style configuration file, `image2_iris.cfg`:

```ini
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
```

first we specify that we want to execute the pipeline defined in `iris_pipeline.pipeline.Image2Pipeline`, then we can
configure each of the steps, for example skip some of them.
Also we can import the configuration of a step from another file, in this case `flat_field.cfg`:

```ini
name = "flat_field" 
class = "jwst.flatfield.FlatFieldStep"

# Optional filename suffix for output flats (only for MOS data).
flat_suffix = None
#override_flat = 'flat.fits'
```

In this file for example we can specify a local FITS file to be used as flat instead of retrieving it from the
Calibration Reference Data System.

## Define the input data

JWST created a specification for defining how input files should be used by a pipeline, it is a JSON file named
an association, see [the JWST documentation](https://jwst-docs.stsci.edu/display/JDAT/Understanding+Associations).

In our example we need to specify a input raw science frame ad a background to be subtracted,
see `asn_subtract_bg_flat.json`:

```json
{
    "asn_rule": "Asn_Lv2Image",
    "asn_pool": "pool",
    "program": "82600",
    "asn_type": "image2",
    "products": [
        {
            "name": "test_iris_subtract_bg_flat",
            "members": [
                {
                    "expname": "sci.fits",
                    "exptype": "science"
                },
                {
                    "expname": "bg.fits",
                    "exptype": "background"
                }
            ]
        }
    ]
}
```

## Execute the pipeline from the command line

We can use `strun` from a terminal to execute the pipeline:

    strun image2_iris.cfg asn_subtract_bg_flat.json

here is the output log:

```bash
2019-02-19 22:26:55,846 - stpipe.Image2Pipeline - INFO - Image2Pipeline instance created.
2019-02-19 22:26:55,847 - stpipe.Image2Pipeline.bkg_subtract - INFO - BackgroundStep instance created.
2019-02-19 22:26:55,849 - stpipe.Image2Pipeline.assign_wcs - INFO - AssignWcsStep instance created.
2019-02-19 22:26:55,850 - stpipe.Image2Pipeline.flat_field - INFO - FlatFieldStep instance created.
2019-02-19 22:26:55,851 - stpipe.Image2Pipeline.photom - INFO - PhotomStep instance created.
2019-02-19 22:26:55,852 - stpipe.Image2Pipeline.resample - INFO - ResampleStep instance created.
2019-02-19 22:26:55,885 - stpipe.Image2Pipeline - INFO - Step Image2Pipeline running with args ('asn_subtract_bg_flat.json',).
2019-02-19 22:26:56,101 - stpipe.Image2Pipeline - INFO - Prefetching reference files for dataset: 'sci.fits' reftypes = ['flat']
2019-02-19 22:26:56,236 - stpipe.Image2Pipeline - INFO - Prefetch for FLAT reference file is '/home/azonca/crds_cache/references/tmt/iris/tmt_iris_flat_0001.fits'.
2019-02-19 22:26:56,372 - stpipe.Image2Pipeline - INFO - Prefetching reference files for dataset: 'bg.fits' reftypes = ['flat']
2019-02-19 22:26:56,391 - stpipe.Image2Pipeline - INFO - Prefetch for FLAT reference file is '/home/azonca/crds_cache/references/tmt/iris/tmt_iris_flat_0001.fits'.
2019-02-19 22:26:56,391 - stpipe.Image2Pipeline - INFO - Starting calwebb_image2 ...
2019-02-19 22:26:56,409 - stpipe.Image2Pipeline - INFO - Processing product test_iris_subtract_bg_flat
2019-02-19 22:26:56,409 - stpipe.Image2Pipeline - INFO - Working on input sci.fits ...
2019-02-19 22:26:56,544 - stpipe.Image2Pipeline.bkg_subtract - INFO - Step bkg_subtract running with args (<ImageModel(2048, 2048) from sci.fits>, ['bg.fits']).
2019-02-19 22:26:58,045 - stpipe.Image2Pipeline.bkg_subtract - INFO - Step bkg_subtract done
2019-02-19 22:26:58,078 - stpipe.Image2Pipeline.assign_wcs - INFO - Step assign_wcs running with args (<ImageModel(2048, 2048) from sci.fits>,).
2019-02-19 22:26:58,079 - stpipe.Image2Pipeline.assign_wcs - INFO - Step skipped.
2019-02-19 22:26:58,079 - stpipe.Image2Pipeline.assign_wcs - INFO - Step assign_wcs done
2019-02-19 22:26:58,101 - stpipe.Image2Pipeline.flat_field - INFO - Step flat_field running with args (<ImageModel(2048, 2048) from sci.fits>,).

2019-02-19 22:26:58,191 - stpipe.Image2Pipeline.flat_field - WARNING - Missing subarray corner/size keywords in reference file
2019-02-19 22:26:58,191 - stpipe.Image2Pipeline.flat_field - WARNING - Setting them to full-frame default values
2019-02-19 22:26:58,306 - stpipe.Image2Pipeline.flat_field - INFO - Step flat_field done
2019-02-19 22:26:58,347 - stpipe.Image2Pipeline.photom - INFO - Step photom running with args (<ImageModel(2048, 2048) from sci.fits>,).
2019-02-19 22:26:58,347 - stpipe.Image2Pipeline.photom - INFO - Step skipped.
2019-02-19 22:26:58,348 - stpipe.Image2Pipeline.photom - INFO - Step photom done
2019-02-19 22:26:58,348 - stpipe.Image2Pipeline - INFO - Finished processing product test_iris_subtract_bg_flat
2019-02-19 22:26:58,349 - stpipe.Image2Pipeline - INFO - ... ending calwebb_image2
2019-02-19 22:26:58,420 - stpipe.Image2Pipeline - INFO - Saved model in test_iris_subtract_bg_flat_cal.fits
2019-02-19 22:26:58,421 - stpipe.Image2Pipeline - INFO - Step Image2Pipeline done
```

We can also notice that `stpipe` accesses the Calibration Reference Data System cache to retrieve the appropriate flat file.
After completion, the reduced science frame `test_iris_subtract_bg_flat_cal.fits` is written to disk, it includes all the metadata
it had initially and additional details about the processing steps that were executed.
