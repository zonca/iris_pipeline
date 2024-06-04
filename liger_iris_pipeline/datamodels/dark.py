from .tmt_reference import TMTReferenceFileModel
from jwst.datamodels.dynamicdq import dynamic_mask

__all__ = ['TMTDarkModel']


class TMTDarkModel(TMTReferenceFileModel):
    """
    A data model for dark reference files.

    Parameters
    __________
    data : numpy float32 array
         Dark current array

    dq : numpy uint16 array
         2-D data quality array for all planes

    err : numpy float32 array
         Error array

    dq_def : numpy table
         DQ flag definitions
    """
    schema_url = "dark.schema.yaml"

    def __init__(self, init=None, **kwargs):
        super().__init__(init=init, **kwargs)

        self.dq = dynamic_mask(self)

        # Implicitly create arrays
        self.dq = self.dq
        self.err = self.err
