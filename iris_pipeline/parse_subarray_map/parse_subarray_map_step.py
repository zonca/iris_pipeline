import numpy as np

from jwst.stpipe import Step
from jwst import datamodels

__all__ = ["ParseSubarrayMapStep"]

SUBARRAY_DQ_BIT = 4


def parse_subarray_map(subarray_map):
    subarray_metadata = []
    for subarray_id in range(1, 10 + 1):
        subarray_indices = np.where(subarray_map == subarray_id)
        if len(subarray_indices[0]) == 0:
            break
        subarray_metadata.append(
            {
                "xstart": int(subarray_indices[1][0] + 1),
                "ystart": int(subarray_indices[0][0] + 1),
                "xsize": int(subarray_indices[1][-1] - subarray_indices[1][0] + 1),
                "ysize": int(subarray_indices[0][-1] - subarray_indices[0][0] + 1),
            }
        )
    return subarray_metadata


class ParseSubarrayMapStep(Step):
    """
    ParseSubarrayMapStep: Parse a subarray map
    extension, if available, and create header metadata
    and data quality flag accordingly
    """

    def process(self, input):

        with datamodels.open(input) as input_model:

            if "subarr_map" in input_model:
                self.log.info("Parsing the SUBARR_MAP extension")
                result = input_model.copy()
                for each in parse_subarray_map(result["subarr_map"]):
                    result.meta.subarray_map.append(each)
                result.dq[result["subarr_map"] != 0] = np.bitwise_or(
                    result.dq[result["subarr_map"] != 0], 2 ** SUBARRAY_DQ_BIT
                )
            else:
                self.log.info("No SUBARR_MAP extension found")
                result = input_model

        return result
