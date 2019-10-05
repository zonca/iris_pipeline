import json
import pytest
import numpy as np
import warnings
import os
from astropy.utils import data
from jwst.associations import load_asn

import iris_pipeline

iris_pipeline.monkeypatch_jwst_datamodels()

from .test_utils import get_data_from_url

def test_image2():
    with open("data/asn_subtract_bg_flat.json") as fp:
        asn = load_asn(fp)
    raw_science_filename = get_data_from_url("17903858")
    raw_background_filename = get_data_from_url("17903855")
    asn["products"][0]["members"][0]["expname"] = raw_science_filename
    asn["products"][0]["members"][1]["expname"] = raw_background_filename
    with open("test_asn.json", "w") as out_asn:
        json.dump(asn, out_asn)
    iris_pipeline.pipeline.Image2Pipeline.call("test_asn.json", config_file="data/image2_iris.cfg")
    ref_filename = get_data_from_url("17903876")
    with iris_pipeline.datamodels.IRISImageModel("test_iris_subtract_bg_flat_cal.fits") as out, \
         iris_pipeline.datamodels.IRISImageModel(ref_filename) as ref:
        np.testing.assert_allclose(out.data, ref.data)
