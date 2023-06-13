import logging
from typing import Dict, Optional, Type

# Class managing list of things.
from dls_utilpack.things import Things

from dls_slurmjob_api.constants import ClassTypes

# Exceptions.
from dls_slurmjob_api.exceptions import NotFound

# Client interface.
from dls_slurmjob_api.interfaces.client import Interface

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------------
__default_dls_slurmjob_restd: Optional[Interface] = None


def dls_slurmjob_restds_set_default(dls_slurmjob_restd: Optional[Interface]):
    global __default_dls_slurmjob_restd
    __default_dls_slurmjob_restd = dls_slurmjob_restd


def dls_slurmjob_restds_get_default() -> Interface:
    global __default_dls_slurmjob_restd
    if __default_dls_slurmjob_restd is None:
        raise RuntimeError("dls_slurmjob_restds_get_default instance is None")
    return __default_dls_slurmjob_restd


# -----------------------------------------------------------------------------------------


class Restds(Things):
    """
    Factory which can make a dls_slurmjob object instance.

    Also can function as named list of objects.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification: Dict) -> Interface:
        """"""

        dls_slurmjob_restd_class = self.lookup_class(specification["type"])

        try:
            dls_slurmjob_restd_object = dls_slurmjob_restd_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to build dls_slurmjob_restd object for type %s"
                % (dls_slurmjob_restd_class)
            ) from exception

        return dls_slurmjob_restd_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type) -> Type:
        """"""

        if class_type == ClassTypes.AIOHTTP:
            from dls_slurmjob_api.restds.aiohttp import Aiohttp

            return Aiohttp

        if class_type == ClassTypes.DUMMY:
            from dls_slurmjob_api.restds.dummy import Dummy

            return Dummy

        raise NotFound(
            "unable to get dls_slurmjob_restd class for type %s" % (class_type)
        )
