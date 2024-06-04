from astropy.io import registry

from .cube import CubeModel
from .liger_iris_image import LigerIrisImageModel
from .ramp import RampModel
from .mask import MaskModel
from .flat import FlatModel
from .dark import DarkModel
from .reference import (
    ReferenceImageModel,
    ReferenceCubeModel,
    ReferenceQuadModel,
    ReferenceFileModel,
)


__all__ = [
    "CubeModel",
    "LigerIrisImageModel",
    "RampModel",
    "MaskModel",
    "ReferenceImageModel",
    "FlatModel",
    "DarkModel",
    "ReferenceCubeModel",
    "ReferenceQuadModel",
    "ReferenceFileModel",
]

_all_models = __all__
_local_dict = locals()
_defined_models = {k: _local_dict[k] for k in _all_models}

def monkeypatch_jwst_datamodels():
    import jwst.datamodels

    jwst.datamodels._defined_models.update(_defined_models)
