#! /usr/bin/env python

from jwst.stpipe import Step
from jwst import datamodels
from ..drsrop_clib import uptheramp_c,mcds_c,nonlin_c
import numpy as np
from astropy.io import fits

__all__ = ["NonlincorrStep"]


class NonlincorrStep(Step):
    """
    ReadoutsampStep:  Sampling
    """

    spec = """
        sigma = float(default=3.0)  # Clipping threshold
        maxiters = integer(default=None)  # Number of clipping iterations
    """

    def process(self, input):

        """
        Step for Nonlinearity Correction
        """

        # Load the input data model
        with datamodels.open(input) as input_model:
            #c0= fits.getdata('/home/arun/coeff_nonlin/coeff0.fits').astype(np.float32)                        
            c0= fits.getdata('coeff0.fits').astype(np.float32)
            c1= fits.getdata('coeff1.fits').astype(np.float32)
            c2= fits.getdata('coeff2.fits').astype(np.float32)
            c3= fits.getdata('coeff3.fits').astype(np.float32)
            c4= fits.getdata('coeff4.fits').astype(np.float32)
            
                        
                        
                        
            # Get the reference file names
            result = input_model.data[0,:,:,:].astype(np.int32)
            time_arr=np.array([0,1000,2000,3000],dtype=np.int32)
            result=nonlin_c(result,time_arr,c0,c1,c2,c3,c4)            
            #result = uptheramp_c(result,time_arr)
            result=result.astype(np.int32)
            result=np.array([result])
            result = datamodels.RampModel(data=result)
            result.update(input_model)
                

        return result
