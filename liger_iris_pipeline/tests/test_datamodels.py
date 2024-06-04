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


from liger_iris_pipeline.datamodels import LigerIrisImageModel


# In[ ]:


raw_science_filename = get_data_from_url("17903858")


# In[ ]:


input_model = LigerIrisImageModel(raw_science_filename)