"""
The version of the package can be returned as a single string or a dict.

When a string, it comes from the package __version__.
When a dict, it also has __version__,
as well as versions of other depdency packages.
"""

from typing import Optional

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

    try:
        import dls_utilpack.version

        meta.update(dls_utilpack.version.meta())
    except Exception:
        meta["dls_utilpack"] = "unavailable"

    try:
        import dls_mainiac_lib.version

        meta.update(dls_mainiac_lib.version.meta())
    except Exception:
        meta["dls_mainiac_lib"] = "unavailable"

    try:
        import dls_multiconf_lib.version

        meta.update(dls_multiconf_lib.version.meta())
    except Exception:
        meta["dls_multiconf_lib"] = "unavailable"

    try:
        import aiohttp

        aiohttp.__version__
        meta["aiohttp"] = aiohttp.__version__
    except Exception:
        meta["aiohttp"] = "unavailable"

    if given_meta is not None:
        given_meta.update(meta)
    else:
        given_meta = meta
    return given_meta
