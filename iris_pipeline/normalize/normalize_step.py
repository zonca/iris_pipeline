from jwst.stpipe import Step
from jwst import datamodels
from . import normalize


__all__ = ["NormalizeStep"]


class NormalizeStep(Step):
    """
    DarkCurrentStep: Performs dark current correction by subtracting
    dark current reference data from the input science data model.
    """

    spec = """
        dark_output = output_file(default = None) # Dark model subtracted
    """

    def process(self, input):

        method = "median"

        with datamodels.open(input) as input_model:

            result = normalize.do_correction(
                input_model, method=method
            )

        return result
