from .model_base import LigerIrisDataModel


__all__ = ['RampModel']


class RampModel(LigerIrisDataModel):
    """
    A data model for 4D ramps.

    Parameters
    __________
    data : numpy float32 array
         The science data

    pixeldq : numpy uint32 array
         2-D data quality array for all planes

    groupdq : numpy uint8 array
         4-D data quality array for each plane

    err : numpy float32 array
         Error array

    zeroframe : numpy float32 array
         Zeroframe array

    group : numpy table
         group parameters table

    int_times : numpy table
         table of times for each integration

    """
    schema_url = "https://oirlab.github.io/schemas/ramp.schema"

    def __init__(self, init=None, **kwargs):
        super(RampModel, self).__init__(init=init, **kwargs)

        # Implicitly create arrays
        self.pixeldq = self.pixeldq
        self.groupdq = self.groupdq
        self.err = self.err