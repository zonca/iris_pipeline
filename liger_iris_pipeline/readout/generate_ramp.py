import pytest
import numpy as np

from jwst.ramp_fitting.ramp_fit import ramp_fit
from jwst.datamodels import dqflags
from jwst.datamodels import MIRIRampModel
from jwst.datamodels import RampModel
from jwst.datamodels import GainModel, ReadnoiseModel


def setup_inputs(ngroups=4, readnoise=10, nints=1,
                 nrows=4096, ncols=4096, nframes=1, grouptime=1.0,gain=1, deltatime=1):
        arr=np.array([np.zeros([4096,4096]),np.ones([4096,4096])*4000,np.ones([4096,4096])*8000,np.ones([4096,4096])*12000],dtype=np.float64)
        arr=np.array([arr])        

        
        times = np.array(list(range(ngroups)),dtype=np.float64) * deltatime
        gain = np.ones(shape=(nrows, ncols), dtype=np.float64) * gain
        err = np.ones(shape=(nints, ngroups, nrows, ncols), dtype=np.float64)
        data = np.zeros(shape=(nints, ngroups, nrows, ncols), dtype=np.float64)
        data=arr
        pixdq = np.zeros(shape=(nrows, ncols), dtype= np.float64)
        read_noise = np.full((nrows, ncols), readnoise, dtype=np.float64)
        gdq = np.zeros(shape=(nints, ngroups, nrows, ncols), dtype=np.int32)
        model1 = RampModel(data=data, err=err, pixeldq=pixdq, groupdq=gdq, times=times)
        model1.meta.instrument.name='MIRI'
        model1.meta.instrument.detector='MIRIMAGE'
        model1.meta.instrument.filter='F480M'
        model1.meta.observation.date='2015-10-13'
        model1.meta.exposure.type='MIR_IMAGE'
        model1.meta.exposure.group_time = deltatime
        model1.meta.subarray.name='FULL'
        model1.meta.subarray.xstart=1
        model1.meta.subarray.ystart = 1
        model1.meta.subarray.xsize = 10
        model1.meta.subarray.ysize = 10
        model1.meta.exposure.frame_time =deltatime
        model1.meta.exposure.ngroups = ngroups
        model1.meta.exposure.group_time = deltatime
        model1.meta.exposure.nframes = 1
        model1.meta.exposure.groupgap = 0
        model1.times=times
        gain = GainModel(data=gain)
        gain.meta.instrument.name='MIRI'
        gain.meta.subarray.xstart = 1
        gain.meta.subarray.ystart = 1
        gain.meta.subarray.xsize = 10
        gain.meta.subarray.ysize = 10
        rnModel = ReadnoiseModel(data=read_noise)
        rnModel.meta.instrument.name='MIRI'
        rnModel.meta.subarray.xstart = 1
        rnModel.meta.subarray.ystart = 1
        rnModel.meta.subarray.xsize = 10
        rnModel.meta.subarray.ysize = 10
        return model1, gdq, rnModel, pixdq, err, gain

model1, gdq, rnModel, pixdq, err, gain = setup_inputs()
model1.to_fits('test_ramp.fits')
