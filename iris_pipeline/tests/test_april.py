import iris_pipeline
iris_pipeline.monkeypatch_jwst_datamodels()  
iris_pipeline.__file__
import numpy as np
from test_utils import get_data_from_url
from jwst import datamodels
from iris_pipeline.dark_current.dark_sub import do_correction
raw_science_filename = get_data_from_url("17903858")
input_model = datamodels.open(raw_science_filename)
