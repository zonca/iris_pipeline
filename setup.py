#!/usr/bin/env python

from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy

sourcefiles = [
    "liger_iris_pipeline/drsrop_clib/_drsrop_clib.pyx",
    #    "liger_iris_pipeline/drsrop_clib/_drsrop_clib.c",
]

extensions = [
    Extension(
        "liger_iris_pipeline.drsrop_clib._drsrop_clib",
        sourcefiles,
        include_dirs=[numpy.get_include(), "/usr/include/cfitsio"],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )
]

setup(ext_modules=cythonize(extensions))
