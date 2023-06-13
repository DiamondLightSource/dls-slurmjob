import argparse
import asyncio

# Use standard logging in this module.
import logging

from dls_utilpack.describe import describe
from dls_utilpack.require import require

# Slurmjob client context creator.
from dls_slurmjob_api.restds.context import Context as DlsSlurmjobRestdClientContext

# Base class for cli subcommands.
from dls_slurmjob_cli.subcommands.base import ArgKeywords, Base

logger = logging.getLogger()


# --------------------------------------------------------------
class QueryJobs(Base):
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

        # Open the slurmjob client context connects to the service process.
        async with client_context as client:
            # Get jobs.
            jobs_dict = await client.query_jobs(self._args.job_ids)

            print(describe("jobs", jobs_dict))

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
            "job_ids",
            nargs="+",
            type=int,
            help="List of jobs.",
            metavar="job_id",
            default=None,
        )

        return parser
