import os

import copy
import datetime
import os
import sys
import warnings

import numpy as np

from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS

import asdf
from asdf import AsdfFile
from asdf import yamlutil
from asdf import schema as asdf_schema
from asdf.tags.core.ndarray import numpy_dtype_to_asdf_datatype

from jwst.datamodels import filetype
from jwst.datamodels import fits_support
from jwst.datamodels import properties
from jwst.datamodels import schema as mschema

from jwst.datamodels.model_base import DataModel
from .extension import BaseExtension
from asdf.extension import AsdfExtension


class TMTDataModel(DataModel):
    """
    Base class of all of the data models.
    """
    schema_url = "core.schema.yaml"

    def __init__(self, init=None, schema=None, extensions=None,
                 pass_invalid_values=False, strict_validation=False,
                 **kwargs):
        """
        Gets the path to the schema using a different prefix then calls the constructor of DataModel
        
        Parameters
        ----------
        init : shape tuple, file path, file object, astropy.io.fits.HDUList, numpy array, None

            - None: A default data model with no shape

            - shape tuple: Initialize with empty data of the given
              shape

            - file path: Initialize from the given file (FITS or ASDF)

            - readable file object: Initialize from the given file
              object

            - ``astropy.io.fits.HDUList``: Initialize from the given
              `~astropy.io.fits.HDUList`.

            - A numpy array: Used to initialize the data array

            - dict: The object model tree for the data model

        schema : tree of objects representing a JSON schema, or string naming a schema, optional
            The schema to use to understand the elements on the model.
            If not provided, the schema associated with this class
            will be used.

        extensions: classes extending the standard set of extensions, optional.
            If an extension is defined, the prefix used should be 'url'.

        pass_invalid_values: If true, values that do not validate the schema
            will be added to the metadata. If false, they will be set to None

        strict_validation: if true, an schema validation errors will generate
            an excption. If false, they will generate a warning.

        kwargs: Aadditional arguments passed to lower level functions
        """

        URL_PREFIX = "http://oirlab.ucsd.edu/schemas/"
        # Load the schema files
        if schema is None:
            schema_path = os.path.join(URL_PREFIX, self.schema_url)
            # Create an AsdfFile so we can use its resolver for loading schemas
            asdf_file = AsdfFile()
            schema = asdf_schema.load_schema(schema_path,
                                             resolver=asdf_file.resolver,
                                             resolve_references=True)
        super().__init__(init=init, schema=schema, extensions=extensions,
                 pass_invalid_values=pass_invalid_values, strict_validation=strict_validation,
                 **kwargs)
