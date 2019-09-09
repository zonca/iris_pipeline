#
#  Module for dark subtracting science data sets
#

import numpy as np
import logging
from jwst import datamodels

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def do_correction(input_model, method="median"):
    """
    Short Summary
    -------------
    Execute all tasks for Dark Current Subtraction

    Parameters
    ----------
    input_model: data model object
        science data to be corrected

    dark_model: dark model object
        dark data

    dark_output: string
        file name in which to optionally save averaged dark data

    Returns
    -------
    output_model: data model object
        dark-subtracted science data

    """

    output_model = apply_norm(input_model, method)

    output_model.meta.cal_step.normalize = 'COMPLETE'

    return output_model


def apply_norm(input, method):
    """
    Subtracts dark current data from science arrays, combines
    error arrays in quadrature, and updates data quality array based on
    DQ flags in the dark arrays.

    Parameters
    ----------
    input: data model object
        the input science data

    dark: dark model object
        the dark current data

    Returns
    -------
    output: data model object
        dark-subtracted science data

    """

    log.debug("normalize: size=%d,%d",
              input.data.shape[0], input.data.shape[1])

    # Create output as a copy of the input science data model
    output = input.copy()

    func = getattr(np, method)
    output.data /= func(output.data)

    return output
