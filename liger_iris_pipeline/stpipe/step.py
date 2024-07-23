from jwst.stpipe import Step
from jwst import datamodels
import stdatamodels


class LigerIrisStep(Step):

    # FIXME - This will need to be ported to a new LigerIrisStep class
    # I do not understand why this is necessary, in JWST it seems like
    # this is not needed and works out of the box.
    # Without this, the pipeline tries to call `datamodes.open` on a
    # file that is already open, which gives the error:
    # expected str, bytes or os.PathLike object, not LigerIrisDataModel
    @classmethod
    def _datamodels_open(cls, init, **kwargs):
        if issubclass(init.__class__, stdatamodels.model_base.DataModel):
            return init
        else:
            return datamodels.open(init, **kwargs)
