import pytest
import numpy as np
import warnings
import os
from astropy.utils import data

import iris_pipeline

iris_pipeline.monkeypatch_jwst_datamodels()


PREDEFINED_DATA_FOLDERS=["iris_pipeline/tests/data/"]
DATAURL="https://tmt-test-data.s3-us-west-1.amazonaws.com/iris_pipeline/"

def get_data_from_url(filename):
    """Retrieves input templates from remote server,
    in case data is available in one of the PREDEFINED_DATA_FOLDERS defined above,
    e.g. at NERSC, those are directly returned."""

    for folder in PREDEFINED_DATA_FOLDERS:
        full_path = os.path.join(folder, filename)
        if os.path.exists(full_path):
            warnings.warn(f"Access data from {full_path}")
            return full_path
    with data.conf.set_temp("dataurl", DATAURL), data.conf.set_temp(
        "remote_timeout", 30
    ):
        warnings.warn(f"Retrieve data for {filename} (if not cached already)")
        local_path = data.get_pkg_data_filename(filename, show_progress=True)
    return local_path

def test_image2():
    iris_pipeline.pipeline.Image2Pipeline.call("iris_pipeline/tests/data/asn_subtract_bg_flat.json", config_file="iris_pipeline/tests/data/image2_iris.cfg")
    ref_filename = get_data_from_url("reference_test_iris_subtract_bg_flat_cal.fits")
    with iris_pipeline.datamodels.IRISImageModel("test_iris_subtract_bg_flat_cal.fits") as out, \
         iris_pipeline.datamodels.IRISImageModel(ref_filename) as ref:
        np.testing.assert_allclose(out.data, ref.data)
