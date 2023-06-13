import logging
import os
import subprocess

# The package version.
from dls_slurmjob_cli.version import meta as version_meta

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestCliDummy:
    """
    Test that we can do a basic database operation through the service on mysql databases.
    """

    def test(self, constants, logging_setup, output_directory):

        configuration_file = "tests/configurations/dummy.yaml"
        CliTester(configuration_file).main(
            constants, configuration_file, output_directory
        )


# ----------------------------------------------------------------------------------------
class CliTester(BaseTester):
    """
    Class to test the dataface.
    """

    def __init__(self, configuration_file):
        BaseTester.__init__(self)

        self.__configuration_file = configuration_file

    async def _main_coroutine(self, constants, specification, output_directory):
        """ """
        # Cause some coverage in the library.
        version_meta()

        # Command to run the service.
        dls_slurmjob_server_cli = [
            "python",
            "-m",
            "dls_slurmjob_cli.main",
            "query_jobs",
            "123",
            "456",
            "--verbose",
            "--configuration",
            self.__configuration_file,
        ]

        # Let the output_directory symbol be replaced in the multiconf.
        os.environ["output_directory"] = output_directory

        # Launch the service as a process.
        logger.debug(f"launching {' '.join(dls_slurmjob_server_cli)}")
        process = subprocess.Popen(
            dls_slurmjob_server_cli,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            # Wait for the process to finish and get the output.
            stdout_bytes, stderr_bytes = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout_bytes, stderr_bytes = process.communicate()

        # Get the return code of the process
        return_code = process.returncode
        logger.debug(f"server return_code is {return_code}")

        if len(stderr_bytes) > 0:
            logger.debug(
                f"================================== server stderr is:\n{stderr_bytes.decode()}"
            )
        if len(stdout_bytes) > 0:
            logger.debug(
                f"================================== server stdout is:\n{stdout_bytes.decode()}"
            )
        if len(stderr_bytes) > 0 or len(stdout_bytes) > 0:
            logger.debug("================================== end of server output")

        assert return_code == 0
