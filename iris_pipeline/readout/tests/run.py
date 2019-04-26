import os
from iris_pipeline.pipeline import ROPPipeline
ROPPipeline.call('sample_ramp.fits', config_file="sampling.cfg")
