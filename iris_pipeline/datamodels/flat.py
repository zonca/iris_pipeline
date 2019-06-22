from .tmt_reference import TMTReferenceFileModel
from jwst.datamodels.dynamicdq import dynamic_mask


__all__ = ['TMTFlatModel']


class TMTFlatModel(TMTReferenceFileModel):
    """
    A data model for 2D flat-field images.

    Parameters
    __________
    data : numpy float32 array
         The science data

    dq : numpy uint32 array
         Data quality array

    err : numpy float32 array
         Error array

    dq_def : numpy table
         DQ flag definitions
    """
    schema_url = "flat.schema.yaml"

    def __init__(self, init=None, **kwargs):
        super().__init__(init=init, **kwargs)

        self.dq = dynamic_mask(self)

        # Implicitly create arrays
        self.dq = self.dq
        self.err = self.err
