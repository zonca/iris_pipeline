#! /usr/bin/env python

from jwst.stpipe import Step
from jwst import datamodels
from drsrop_clib import uptheramp_c,mcds_c,nonlin_c
import numpy as np

__all__ = ["ReadoutsampStep"]


class ReadoutsampStep(Step):
    """
    ReadoutsampStep:  Sampling
    """

    spec = """
        sigma = float(default=3.0)  # Clipping threshold
        maxiters = integer(default=None)  # Number of clipping iterations
        mode= string(default='utr')
    """

    def process(self, input):

        """
        Sampling step.
        Currently 3 Sampling modes
         -- CDS
         -- MCDS
         -- UTR
        """

        # Load the input data model
        with datamodels.open(input) as input_model:

            # Get the reference file names
            result = input_model.data[0,:,:,:].astype(np.int32)
            time_arr=np.array([0,1000,2000,3000],dtype=np.int32)
            if(self.mode=='mcds'):
                    self.log.info("MCDS Sampling Selected")
                    result = mcds_c(result,time_arr,2)
            else:
                    self.log.info("UTR Sampling Selected")
                    result = utr(result,time_arr,2)
            print(result.shape)
            result = datamodels.ImageModel(data=result)
            result.update(input_model)
                

        return result
