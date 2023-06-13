import logging
from typing import Dict, List

# Client interface.
from dls_slurmjob_api.interfaces.client import Interface

# Job info.
from dls_slurmjob_api.models.job_summary_model import JobSummaryModel

# Openapi job parameters.
from dls_slurmjob_api.models.openapi.v0.field_0 import (
    Field38JobProperties as OpenapiJobProperties,
)

logger = logging.getLogger(__name__)


class Dummy(Interface):
    """
    Object implementing dummy implementation of the slurm rest API.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):
        self.__specification = specification

    # ----------------------------------------------------------------------------------------
    def specification(self):
        return self.__specification

    # ----------------------------------------------------------------------------------------
    async def query_jobs(self, job_ids: List[int]) -> Dict[int, JobSummaryModel]:
        """"""

        job_info_models: Dict[int, JobSummaryModel] = {}

        for job_id in job_ids:
            # Make an object representing the job's info.
            job_info_model = JobSummaryModel(
                job_id=job_id,
                is_finished=True,
                other="dummy",
            )

            job_info_models[job_id] = job_info_model

        return job_info_models

    # ----------------------------------------------------------------------------------------
    async def submit_job(
        self, script_filename: str, properties: OpenapiJobProperties
    ) -> int:
        """
        Submit job to slurm.

        Args:
            script: fully qualified bash script filename to run
            properties: job's properties from the OpenApi specification

        Returns:
            unique job_id within the slurm system
        """

        return 123

    # ----------------------------------------------------------------------------------------
    async def open_client_session(self):
        """"""
        pass

    # ----------------------------------------------------------------------------------------
    async def close_client_session(self):
        """"""
        pass
