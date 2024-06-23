#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import liger_iris_pipeline


# In[ ]:


# check where are we loading the library from
liger_iris_pipeline.__file__


# In[ ]:


import numpy as np


# In[ ]:


from test_utils import get_data_from_url


# In[ ]:


from jwst import datamodels


# In[ ]:


raw_science_filename = get_data_from_url("17903858")


# In[ ]:


input_model = datamodels.open(raw_science_filename)


# In[ ]:


input_model


# In[ ]:


step = liger_iris_pipeline.pipeline.ProcessFlatfieldL2()


# In[ ]:


step_output = step.run(raw_science_filename)


# In[ ]:


dark_current = datamodels.open(step.dark_current.dark_name)


# In[ ]:


expected = input_model.data - dark_current.data
expected /= np.median(expected)


# In[ ]:


np.testing.assert_allclose(step_output[0].data, expected)

