import argparse
import asyncio

# Use standard logging in this module.
import logging
import os

from dls_utilpack.require import require

# Job info.
from dls_slurmjob_api.models.openapi.v0.field_0 import (
    Field38JobProperties as OpenapiJobProperties,
)

# Slurmjob client context creator.
from dls_slurmjob_api.restds.context import Context as DlsSlurmjobRestdClientContext

# Base class for cli subcommands.
from dls_slurmjob_cli.subcommands.base import ArgKeywords, Base

# The package version.
from dls_slurmjob_cli.version import version as dls_slurmjob_version

logger = logging.getLogger()


# --------------------------------------------------------------
class SubmitJob(Base):
    """
    List jobs.
    """

    def __init__(self, args, mainiac):
        super().__init__(args)

    # ----------------------------------------------------------------------------------------
    def run(self):
        """ """

        # Run in asyncio event loop.
        asyncio.run(self.__run_coro())

    # ----------------------------------------------------------
    async def __run_coro(self):
        """
        Run the service as an asyncio coro.
        """

        # Load the configuration.
        multiconf_object = self.get_multiconf(vars(self._args))
        # Resolve the symbols and give configuration as a dict.
        multiconf_dict = await multiconf_object.load()

        # Get the specfication we want by keyword in the full configuration.
        specification = require(
            "configuration",
            multiconf_dict,
            "dls_slurmjob_restd_specification",
        )

        # Make the slurmjob client context from the specification in the configuration.
        client_context = DlsSlurmjobRestdClientContext(specification)

        # These are the minimum required.
        properties = OpenapiJobProperties()
        properties.partition = "cs04r"
        properties.current_working_directory = os.getcwd()
        properties.environment = {"DLS_SLURMJOB": dls_slurmjob_version()}

        # properties.name = "dls_slurmjob_cli"
        # properties.tasks = 1
        # properties.nodes = 1
        # properties.time_limit = "00:01:00"

        # Open the slurmjob client context connects to the service process.
        async with client_context as client:
            # Get jobs.
            job_id = await client.submit_job(self._args.script_filename, properties)

            print(job_id)

    # ----------------------------------------------------------
    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Add arguments for this subcommand.

        This is a static method called from the main program.

        Args:
            parser (argparse.ArgumentParser): Parser object which has been created already.

        """

        parser.add_argument(
            "--configuration",
            "-c",
            help="Configuration file.",
            type=str,
            metavar="filename.yaml",
            default=None,
            dest=ArgKeywords.CONFIGURATION,
        )

        parser.add_argument(
            ArgKeywords.SCRIPT_FILENAME,
            type=str,
            help="Script filename.",
            metavar="filename",
            default=None,
        )

        return parser
