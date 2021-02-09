from astropy.io import registry

from .cube import IRISCubeModel
from .iris import IRISImageModel
from .tmt_ramp import TMTRampModel
from .tmt_mask import TMTMaskModel
from .flat import TMTFlatModel
from .dark import TMTDarkModel
from .tmt_reference import (
    TMTReferenceImageModel,
    TMTReferenceCubeModel,
    TMTReferenceQuadModel,
    TMTReferenceFileModel,
)


__all__ = [
    "IRISCubeModel",
    "IRISImageModel",
    "TMTRampModel",
    "TMTMaskModel",
    "TMTReferenceImageModel",
    "TMTFlatModel",
    "TMTDarkModel",
    "TMTReferenceCubeModel",
    "TMTReferenceQuadModel",
    "TMTReferenceFileModel",
]

_all_models = __all__
_local_dict = locals()
_defined_models = {k: _local_dict[k] for k in _all_models}

def monkeypatch_jwst_datamodels():
    import jwst.datamodels

    jwst.datamodels._defined_models.update(_defined_models)
