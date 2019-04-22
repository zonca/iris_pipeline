from astropy.io import registry

from .iris import IRISImageModel
from .tmt_ramp import TMTRampModel
from .tmt_mask import TMTMaskModel


__all__ = ["IRISImageModel", "TMTRampModel", "TMTMaskModel"]

# Initialize the astropy.io registry,
# but only the first time this module is called

try:
    _defined_models
except NameError:
    with registry.delay_doc_updates(DataModel):
        registry.register_reader("datamodel", DataModel, ndmodel.read)
        registry.register_writer("datamodel", DataModel, ndmodel.write)
        registry.register_identifier("datamodel", DataModel, ndmodel.identify)

_all_models = __all__[1:]
_local_dict = locals()
_defined_models = {k: _local_dict[k] for k in _all_models}
