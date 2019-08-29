import json
import pytest
import numpy as np
import warnings
import os
from astropy.utils import data
from jwst.associations import load_asn

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
    with open("iris_pipeline/tests/data/asn_subtract_bg_flat.json") as fp:
        asn = load_asn(fp)
    raw_science_filename = get_data_from_url("raw_science_frame_sci.fits")
    raw_background_filename = get_data_from_url("raw_background_frame_cal.fits")
    asn["products"][0]["members"][0]["expname"] = raw_science_filename
    asn["products"][0]["members"][1]["expname"] = raw_background_filename
    with open("test_asn.json", "w") as out_asn:
        json.dump(asn, out_asn)
    iris_pipeline.pipeline.Image2Pipeline.call("test_asn.json", config_file="iris_pipeline/tests/data/image2_iris.cfg")
    ref_filename = get_data_from_url("reference_test_iris_subtract_bg_flat_cal.fits")
    with iris_pipeline.datamodels.IRISImageModel("test_iris_subtract_bg_flat_cal.fits") as out, \
         iris_pipeline.datamodels.IRISImageModel(ref_filename) as ref:
        np.testing.assert_allclose(out.data, ref.data)
