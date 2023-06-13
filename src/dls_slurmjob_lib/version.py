"""
The version of the package can be returned as a single string or a dict.

When a string, it comes from the package __version__.
When a dict, it also has __version__,
as well as versions of other depdency packages.
"""

from typing import Optional

import dls_mainiac_lib.version
import dls_normsql.version
import dls_utilpack.version

from dls_slurmjob_lib import __version__ as dls_slurmjob_lib_version


# ----------------------------------------------------------
def version() -> str:
    """
    Version of the dls_normsql package as a string.
    """

    return dls_slurmjob_lib_version


# ----------------------------------------------------------
def meta(given_meta: Optional[dict] = None) -> dict:
    """
    Returns version information from the dls_normsql package
    and its dependencies as a dict.
    Adds version information to a given meta dict if it was provided.
    """

    meta = {}
    meta["dls_slurmjob_lib"] = version()
    meta.update(dls_mainiac_lib.version.meta())
    meta.update(dls_normsql.version.meta())
    meta.update(dls_utilpack.version.meta())

    try:
        import setproctitle

        setproctitle.__version__
        meta["setproctitle"] = setproctitle.__version__
    except Exception:
        meta["setproctitle"] = "unavailable"

    if given_meta is not None:
        given_meta.update(meta)
    else:
        given_meta = meta
    return given_meta
