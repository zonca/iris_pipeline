import os
import iris_pipeline

iris_pipeline.monkeypatch_jwst_datamodels()


def test_rop1():
    iris_pipeline.pipeline.ROPPipeline.call(
        "iris_pipeline/tests/data/test_ramp.fits", config_file="iris_pipeline/tests/data/drsrop.cfg"
    )
