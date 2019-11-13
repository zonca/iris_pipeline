#! /usr/bin/env python

from jwst.stpipe import Step
from jwst import datamodels
from . import subtract_images


class SubtractImagesStep(Step):
    """
    SubtractImagesStep:  Subtract two exposures from one
    another to accomplish background subtraction.
    """

    spec = """
    """

    def process(self, input1, input2):

        """
        Subtract the background signal from a data model by
        subtracting a background image from it.

        Parameters
        ----------
        input1: data model
            input science data model to be background-subtracted

        input2: data model
            background data model

        Returns
        -------
        result: data model
            background-subtracted science data model
        """

        # Open the first input
        model1 = datamodels.open(input1)

        if isinstance(model1, datamodels.CubeModel):
            self.log.debug("Input is a CubeModel")
        elif isinstance(model1, datamodels.ImageModel):
            self.log.debug("Input is an ImageModel")

        # Assume that the second input model is always an ImageModel
        model2 = datamodels.ImageModel(input2)

        # Call the subtraction routine
        result = subtract_images.subtract(model1, model2)

        # Set the step status indicator in the output model
        result.meta.cal_step.back_sub = "COMPLETE"

        # We're done. Close the models and return the result.
        model1.close()
        model2.close()

        return result
