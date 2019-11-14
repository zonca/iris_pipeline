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

    Returns
    -------
    output: data model object
        normalized frame

    """

    log.debug("normalize: size=%d,%d", input.data.shape[0], input.data.shape[1])

    # Create output as a copy of the input science data model
    output = input.copy()

    func = getattr(np, method)
    output.data /= func(output.data)

    return output
