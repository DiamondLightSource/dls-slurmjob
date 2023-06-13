import logging
import os
from typing import Optional

# Configurator.
from dls_multiconf_lib.constants import ThingTypes as MulticonfThingTypes
from dls_multiconf_lib.multiconfs import Multiconfs, multiconfs_set_default

# Environment variables with some extra functionality.
from dls_slurmjob_lib.envvar import Envvar

logger = logging.getLogger(__name__)


class ArgKeywords:
    CONFIGURATION = "configuration"
    SCRIPT_FILENAME = "script_filename"


class Base:
    """
    Base class for subcommands.  Handles details like configuration.
    """

    def __init__(self, args):
        self._args = args

        self.__temporary_directory = None

    # ----------------------------------------------------------------------------------------
    def get_multiconf(self, args_dict: dict):

        dls_slurmjob_multiconf = self.build_object_from_environment(args_dict=args_dict)

        substitutions = {
            "CWD": os.getcwd(),
            "HOME": os.environ.get("HOME", "HOME"),
            "USER": os.environ.get("USER", "USER"),
            "PATH": os.environ.get("PATH", "PATH"),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "PYTHONPATH"),
            "output_directory": os.environ.get("output_directory", "output_directory"),
        }

        dls_slurmjob_multiconf.substitute(substitutions)

        # Set this as the default multiconf so it is available everywhere.
        multiconfs_set_default(dls_slurmjob_multiconf)

        return dls_slurmjob_multiconf

    # ----------------------------------------------------------------------------------------
    def build_object_from_environment(
        self,
        environ: Optional[dict] = None,
        args_dict: Optional[dict] = None,
    ):

        configuration_keyword = "configuration"

        multiconf_filename = None

        if args_dict is not None:
            multiconf_filename = args_dict.get(configuration_keyword)

        if multiconf_filename is not None:
            # Make sure the path exists.
            if not os.path.exists(multiconf_filename):
                raise RuntimeError(
                    f"unable to find --{configuration_keyword} file {multiconf_filename}"
                )
        else:
            # Get the explicit name of the config file.
            multiconf_filename = Envvar(
                Envvar.DLS_SLURMJOB_CONFIGFILE,
                environ=environ,
            )

            # Config file is explicitly named?
            if multiconf_filename.is_set:
                # Make sure the path exists.
                multiconf_filename = multiconf_filename.value
                if not os.path.exists(multiconf_filename):
                    raise RuntimeError(
                        f"unable to find {Envvar.DLS_SLURMJOB_CONFIGFILE} {multiconf_filename}"
                    )
            # Config file is not explicitly named?
            else:
                raise RuntimeError(
                    f"command line --{configuration_keyword} not given"
                    f" and environment variable {Envvar.DLS_SLURMJOB_CONFIGFILE} is not set"
                )

        configurator = Multiconfs().build_object(
            {
                "type": MulticonfThingTypes.YAML,
                "type_specific_tbd": {"filename": multiconf_filename},
            }
        )

        configurator.substitute(
            {"configurator_directory": os.path.dirname(multiconf_filename)}
        )

        return configurator
