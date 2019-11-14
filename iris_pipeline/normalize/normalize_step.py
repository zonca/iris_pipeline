from jwst.stpipe import Step
from jwst import datamodels
from . import normalize


__all__ = ["NormalizeStep"]


class NormalizeStep(Step):
    """
    NormalizeStep: Normalize a frame by dividing
    by its own mean or median
    """

    spec = """
        method = string(default='median')
    """

    def process(self, input):

        with datamodels.open(input) as input_model:

            result = normalize.do_correction(input_model, method=self.method)

        return result
