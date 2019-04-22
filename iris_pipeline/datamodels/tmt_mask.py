from .tmt_reference import TMTReferenceFileModel
from jwst.datamodels.dynamicdq import dynamic_mask

__all__ = ['TMTMaskModel']


class TMTMaskModel(TMTReferenceFileModel):
    """
    A data model for 2D masks.

    Parameters
    __________
    dq : numpy uint32 array
         The mask

    dq_def : numpy table
         DQ flag definitions
    """
    schema_url = "tmt_mask.schema.yaml"

    def __init__(self, init=None, **kwargs):
        super().__init__(init=init, **kwargs)

        if self.dq is not None or self.dq_def is not None:
            self.dq = dynamic_mask(self)

        # Implicitly create arrays
        self.dq = self.dq

    def get_primary_array_name(self):
        """
        Returns the name "primary" array for this model, which
        controls the size of other arrays that are implicitly created.
        This is intended to be overridden in the subclasses if the
        primary array's name is not "data".
        """
        return 'dq'
