# Imports
import liger_iris_pipeline
liger_iris_pipeline.monkeypatch_jwst_datamodels()
import numpy as np
from astropy.io import fits
from liger_iris_pipeline.tests.test_utils import get_data_from_url
from jwst import datamodels

def test_process_flatfield():

    # Grab raw science
    raw_science_filename = get_data_from_url("17903858")
    with fits.open(raw_science_filename, output_verify='fix', mode='update') as f:
        f[0].header['DATAMODL'] = 'LigerIrisImageModel'
        if len(f[0].header['DATE']) > 22:
            f[0].header['DATE'] = f[0].header['DATE'][:22]
    input_model = datamodels.open(raw_science_filename)

    # Initialize flatfield pipeline
    pipeline = liger_iris_pipeline.pipeline.ProcessFlatfieldL2()

    # Run pipeline
    pipeline_output = pipeline.run(raw_science_filename)

    breakpoint()

    # Open dark
    dark_current = datamodels.open(pipeline_output[0].dark_current.dark_name)

    # Manually create a master flat
    expected = input_model.data - dark_current.data
    expected /= np.median(expected)

    # Test
    np.testing.assert_allclose(dark_current[0].data, expected)

test_process_flatfield()