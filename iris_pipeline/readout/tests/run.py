import os
import iris_pipeline
print(iris_pipeline.__file__)
iris_pipeline.monkeypatch_jwst_datamodels()
#from iris_pipeline.pipeline import ROPPipeline
iris_pipeline.pipeline.ROPPipeline.call('sample_ramp_new.fits', config_file="sampling.cfg")
