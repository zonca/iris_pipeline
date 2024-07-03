#! /usr/bin/env python
from jwst.stpipe import Step
from jwst import datamodels
from ..datamodels import LigerIrisImageModel
import logging
from .assign_wcs import load_wcs

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

__all__ = ["AssignWcsStep"]


class AssignWcsStep(Step):
    """
    AssignWcsStep: Create a gWCS object and store it in ``Model.meta``.

    Reference file types (none for now):

    distortion         Spatial distortion model (FGS, MIRI, NIRCAM, NIRISS)
    specwcs            Wavelength calibration models (MIRI, NIRCAM, NIRISS)
    wavelengthrange    Typical wavelength ranges (MIRI, NIRCAM, NIRISS, NIRSPEC)

    Parameters
    ----------
    input : `~IRISImageModel` or `IRISImageModel`
        Input model.
    """

    # eventually ['distortion' , 'specwcs', 'wavelengthrange']
    reference_file_types = []

    def process(self, input, *args, **kwargs):
        reference_file_names = {}
        if isinstance(input, str):
            input_model = datamodels.open(input)
        else:
            input_model = input

        # If input type is not supported, log warning, set to 'skipped', exit
        if not (isinstance(input_model, LigerIrisImageModel)):
            log.warning("Input dataset type is not supported.")
            log.warning("assign_wcs expects IRISImageModel as input.")
            log.warning("Skipping assign_wcs step.")
            result = input_model.copy()
            result.meta.cal_step.assign_wcs = "SKIPPED"
        else:
            # Get reference files
            for reftype in self.reference_file_types:
                reffile = self.get_reference_file(input_model, reftype)
                reference_file_names[reftype] = reffile if reffile else ""
            log.debug(f"reference files used in assign_wcs: {reference_file_names}")

            # Assign wcs
            result = load_wcs(input_model, reference_file_names)

        # Close model if opened manually
        if isinstance(input, str):
            input_model.close()

        return result
