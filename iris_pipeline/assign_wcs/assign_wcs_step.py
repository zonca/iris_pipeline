#! /usr/bin/env python
from jwst.stpipe import Step
from .. import datamodels
import logging
from .assign_wcs import load_wcs

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

__all__ = ["AssignWcsStep"]


class AssignWcsStep(Step):
    """
    AssignWcsStep: Create a gWCS object and store it in ``Model.meta``.

    Reference file types:

    distortion         Spatial distortion model (FGS, MIRI, NIRCAM, NIRISS)
    specwcs            Wavelength calibration models (MIRI, NIRCAM, NIRISS)
    wavelengthrange    Typical wavelength ranges (MIRI, NIRCAM, NIRISS, NIRSPEC)

    Parameters
    ----------
    input : `~jwst.datamodels.IRISImageModel`
        Input exposure.
    """

    spec = """
        slit_y_low = float(default=-.55)  # The lower edge of a slit.
        slit_y_high = float(default=.55)  # The upper edge of a slit.

    """

    reference_file_types = [] # ['distortion', 'specwcs', 'wavelengthrange']

    def process(self, input, *args, **kwargs):
        reference_file_names = {}
        with datamodels.open(input) as input_model:
            # If input type is not supported, log warning, set to 'skipped', exit
            if not (isinstance(input_model, datamodels.IRISImageModel)):
                log.warning("Input dataset type is not supported.")
                log.warning("assign_wcs expects IRISImageModel as input.")
                log.warning("Skipping assign_wcs step.")
                result = input_model.copy()
                result.meta.cal_step.assign_wcs = 'SKIPPED'
                return result

            for reftype in self.reference_file_types:
                reffile = self.get_reference_file(input_model, reftype)
                reference_file_names[reftype] = reffile if reffile else ""
            log.debug(f'reference files used in assign_wcs: {reference_file_names}')

            slit_y_range = [self.slit_y_low, self.slit_y_high]
            result = load_wcs(input_model, reference_file_names, slit_y_range)


        return result
