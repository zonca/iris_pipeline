# %%
import liger_iris_pipeline

liger_iris_pipeline.monkeypatch_jwst_datamodels()  

# %%
liger_iris_pipeline.__file__

# %%
import numpy as np

# %%
from test_utils import get_data_from_url

# %%
from jwst import datamodels

# %%
from liger_iris_pipeline.dark_current.dark_sub import do_correction

# %% [markdown]
# ## Lower level functions
# 
# * `do_correction`

# %%
raw_science_filename = "raw.fits"

# %%
input_model = datamodels.open(raw_science_filename)

# %%
input_model

# %%
input_model.data.max()

# %%
np.random.seed(100)

# %%
dark_model = liger_iris_pipeline.datamodels.DarkModel(data=np.random.normal(size=(4096, 4096)))

# %%
expected_output_data = input_model.data - dark_model.data

# %%
output = do_correction(input_model, dark_model)

# %%
np.testing.assert_allclose(output.data, expected_output_data)

# %% [markdown]
# ## High level step class

# %%
step = liger_iris_pipeline.dark_current.DarkCurrentStep()

# %%
step_output = step.run(raw_science_filename)

# %%
step_dark_model = datamodels.open(step.dark_name)

# %%
np.testing.assert_allclose(step_output.data, input_model.data - step_dark_model.data)