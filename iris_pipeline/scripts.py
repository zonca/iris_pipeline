#!/usr/bin/env python

"""
JWST strun monkeypatched for TMT
"""

import sys
import iris_pipeline
iris_pipeline.monkeypatch_jwst_datamodels()

from jwst.assign_wcs.util import NoDataOnDetectorError
from jwst.stpipe import Step

def tmtrun():

    if '--version' in sys.argv:
        sys.stdout.write("%s\n" % iris_pipeline.__version__)
        sys.exit(0)

    try:
        step = Step.from_cmdline(sys.argv[1:])
    except NoDataOnDetectorError:
        import traceback
        traceback.print_exc()
        sys.exit(64)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
