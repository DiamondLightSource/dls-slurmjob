import logging

import dls_mainiac_lib.version

import dls_slurmjob_lib.version

from . import __version__

logger = logging.getLogger(__name__)


# ----------------------------------------------------------
def version():
    """
    Current version.
    """

    return __version__


# ----------------------------------------------------------
def meta(given_meta=None):
    """
    Returns version information as a dict.
    Adds version information to given meta, if any.
    """
    s = {}
    s["dls_slurmjob_cli"] = version()
    s.update(dls_slurmjob_lib.version.meta())
    s.update(dls_mainiac_lib.version.meta())

    if given_meta is not None:
        given_meta.update(s)
    else:
        given_meta = s
    return given_meta
