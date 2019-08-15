import pytest

import iris_pipeline

iris_pipeline.monkeypatch_jwst_datamodels()

def test_image2():
    iris_pipeline.pipeline.Image2Pipeline.call("iris_pipeline/tests/data/asn_subtract_bg_flat.json", config_file="iris_pipeline/tests/data/image2_iris.cfg")
