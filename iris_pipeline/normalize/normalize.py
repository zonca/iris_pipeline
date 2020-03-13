import numpy as np
import logging
from jwst import datamodels

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def do_correction(input_model, method="median"):
    """
    Short Summary
    -------------
    Normalize a frame by dividing by its own mean or median

    Parameters
    ----------

    input_model: data model object
        the input science data

    method: string
        name of numpy method to use for normalization, e.g.
        median (default) or mean

    Returns
    -------
    output_model: data model object
        normalized frame

    """

    output_model = apply_norm(input_model, method)

    output_model.meta.cal_step.normalize = "COMPLETE"

    return output_model


def apply_norm(input, method):
    """
    Divides the input frame by its own median or mean,
    based on the method string.

    Parameters
    ----------
    input: data model object
        the input science data

    method: string
        name of numpy method to use for normalization, e.g.
        median (default) or mean
        mode uses `scipy.stats.mode`

    Returns
    -------
    output: data model object
        normalized frame

    """

    log.debug("normalize: size=%d,%d", input.data.shape[0], input.data.shape[1])

    # Create output as a copy of the input science data model
    output = input.copy()

    valid_data = input.dq == 0

    if valid_data.sum() == 0:  # no valid data
        norm_factor = 1
    else:
        if method == "mode":
            import scipy.stats

            norm_factor = scipy.stats.mode(input.data[valid_data], axis=None)[0][0]
        else:
            norm_factor = getattr(np, method)(input.data[valid_data])

    log.info("running normalize with method %s", method)
    output.data /= norm_factor

    return output
