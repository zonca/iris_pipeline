***************************
Calibration
***************************

Calibration files
=================

Auxiliary data used in DRP algorithms are called calibration data. This includes both on-sky data (that is not of the astronomical target itself), daytime calibration frames, and other sub-component metadata. Metadata is non-image information that will typically come from the header of raw FITS files, or from IRIS, and/or the adaptive optics system via the observatory telemetry service. The NFIRAOS Science Calibration Unit (NSCU) will include a calibration system that will facilitate the taking of
daytime calibration frames, such as arc lamp spectra, white light flat field images, and pinhole grids for measuring distortion. 
The following table summarizes the required calibration files necessary for the Data Reduction Software.

.. csv-table:: Calibration frames
   :header: "Name", "Reference Type", "Source", "Algorithms"
   :widths: 30,20,20,20

   "Atm. Dispersion Residual","Metadata",    "IRIS ADC",              "Atmospheric Correction"
   "Arc lamp spectra*",       "CAL (2D)",    "IRIS DTC (NSCU)",       "Wavelength solution "
   "Bad pixel map",           "CAL (2D)",    "IRIS DTC",              "Correction of detector artifacts"
   "Dark Frame",              "CAL (2D)",    "IRIS DTC and NTC",      "Dark subtraction "
   "Env metadata",            "Metadata",    "ESW, FITS header",      "All"
   "Fiber image",              "CAL (2D, 3D)","IRIS DTC (NSCU)",       "PSF Calibration"
   "Flux calibration star",   "CAL (2D, 3D)","IRIS On-sky",           "Extract Star, Remove Absorption Lines"
   "Instrument config",       "Metadata",    "ESW, FITS header",      "All"
   "Lenslet scan*",           "Rect Matrix CAL (2D)", "IRIS DTC (NSCU)","Spectral Extraction"
   "NFIRAOS config",          "Metadata",    "ESW, FITS header",      "All"
   "Pinhole Grid (D-Map)",    "CAL (2D)",    "IRIS DTC (NSCU)",       "Field distortion correction"
   "PSF metadata",            "Metadata ",   "ESW, FITS header",      "PSF calibration"
   "PSF star",                "CAL (2D, 3D)","IRIS on-sky ",          "PSF calibration"
   "Sky frame",               "CAL (2D, 3D)","IRIS on-sky",           "Sky-subtraction"
   "Telescope config PTG",    "Metadata ",   "ESW, FITS header",      "All "


Access calibration files via the Calibration Reference Data System (CRDS)
=========================================================================

The `Calibration Reference Data System
(CRDS) <https://hst-crds.stsci.edu/static/users_guide/overview.html>`_
is a set of tools developed by Space Telescope to organize and retrieve
calibration reference files, e.g. flat frames, dark frames, for JWST and
HST. When ``stpipe`` is executing a pipeline, it can automatically
connect to the JWST CRDS server and get the right flat based on the
metadata in the header of the data FITS files. The logic necessary to
choose the right file is encoded in text files. Those configuration
files and the actual calibration FITS files are also cached locally so
that the CRDS client library works even without any connection to a
central server.

We have created a CRDS cache folder in the Github repository
https://github.com/oirlab/tmt-crds-cache,
this includes in the ``mappings/tmt``
`folder <https://github.com/oirlab/tmt-crds-cache/tree/master/mappings/tmt>`_
the metadata for IRIS and the rules to choose the right flat-field
frame, for now there is only a dummy rule but this can be easily
customize querying the metadata in the input file.

Currently we do not have any CRDS server running, but the users can
download the CRDS cache locally and use it anyway, see the `Getting
started <getting-started>`_ documentation.

Also, the CRDS client library needs to have minimal knowledge about
metadata for TMT, therefore we maintain a fork of that library which
simply adds a submodule dedicated to IRIS, https://github.com/oirlab/tmt-crds, it is quite
easy to upgrade this to newer releases of CRDS by Space Telescope.

If TMT decided to use CRDS as their Data Management System, it would
leverage the extensive set of tools and documentation available and
would not require modifications to ``stpipe``; otherwise, we will
implement support for the DMS API into (our own fork of) ``stpipe``.
