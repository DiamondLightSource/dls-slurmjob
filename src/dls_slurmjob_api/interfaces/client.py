import logging
from abc import ABC, abstractmethod
from typing import Dict, List

# Job info.
from dls_slurmjob_api.models.job_summary_model import JobSummaryModel

logger = logging.getLogger(__name__)


class Interface(ABC):
    """
    Object implementing the dls_slurmjob API.
    """

    # ----------------------------------------------------------------------------------------
    @abstractmethod
    def specification(self):
        return self.__specification

    # ----------------------------------------------------------------------------------------
    @abstractmethod
    async def query_jobs(self, job_ids: List[int]) -> Dict[int, JobSummaryModel]:
        """
        Query slurm for info on the given list of jobs.

        Args:
            job_ids: list of at least one job_id integers

        Returns:
            infos the same length and sequence as the given job_ids
        """
        pass

    # ----------------------------------------------------------------------------------------
    @abstractmethod
    async def open_client_session(self):
        """"""
        pass

    # ----------------------------------------------------------------------------------------
    @abstractmethod
    async def close_client_session(self):
        """"""
        pass
