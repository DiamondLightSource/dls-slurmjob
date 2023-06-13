import copy
import json
import logging
from typing import Dict, List

from dls_utilpack.callsign import callsign
from dls_utilpack.describe import describe

# Class for an aiohttp client.
from dls_slurmjob_api.aiohttp_client import AiohttpClient

# Job rejected by slurm engine, for example missing some required property.
from dls_slurmjob_api.exceptions import Rejected

# Client interface.
from dls_slurmjob_api.interfaces.client import Interface

# Job info.
from dls_slurmjob_api.models.job_summary_model import JobSummaryModel
from dls_slurmjob_api.models.openapi.v0.field_0 import (
    Field38JobProperties as OpenapiJobProperties,
)
from dls_slurmjob_api.models.openapi.v0.field_0 import (
    Field38JobSubmission as OpenapiJobSubmission,
)
from dls_slurmjob_api.models.openapi.v0.field_0 import (
    Field38JobSubmissionResponse as OpenapiJobSubmissionResponse,
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class Aiohttp(AiohttpClient, Interface):
    """
    Object implementing client side API for talking to the dls_slurmjob_restd server.
    """

    FINISHED_JOB_STATE_UNKNOWN = "UNKNOWN"

    FINISHED_JOB_STATES = [
        "COMPLETED",  # The job has successfully completed execution.
        "CANCELLED",  # The job was canceled by the user or the system administrator before completion.
        "FAILED",  # The job encountered an error during execution and did not complete successfully.
        "TIMEOUT",  # The job exceeded its time limit and was terminated by the system.
        "NODE_FAIL",  # One or more nodes allocated to the job have failed, leading to job termination.
        "OUT_OF_MEMORY",  # The job exceeded the memory limits and was terminated.
        "PREEMPTED",  # The job was preempted by a higher-priority job or system event.
        FINISHED_JOB_STATE_UNKNOWN,  # We didn't find the job in the query response.
    ]

    UNFINISHED_JOB_STATES = [
        "PENDING",  # The job is waiting to be scheduled and has not started running yet.
        "RUNNING",  # The job is currently running on a compute node.
        "SUSPENDED",  # The job has been suspended and is temporarily halted. This can happen if the job exceeds resource limits or due to user intervention.
        "COMPLETING",  # The job has finished running, but some post-processing or cleanup tasks are still in progress.
    ]

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):

        # We will get an umbrella specification which must contain an aiohttp_specification within it.
        AiohttpClient.__init__(
            self,
            specification["type_specific_tbd"]["aiohttp_specification"],
        )

    # ----------------------------------------------------------------------------------------
    def specification(self):
        return self.__specification

    # ----------------------------------------------------------------------------------------
    async def query_jobs(self, job_ids: List[int]) -> Dict[int, JobSummaryModel]:
        """
        Query slurm for info on the given list of jobs.

        Args:
            job_ids: list of at least one job_id integers

        Returns:
            infos the same length and sequence as the given job_ids
        """

        is_client_connection_possible = await self.is_client_connection_possible()

        if not is_client_connection_possible:
            raise RuntimeError(
                f"{callsign(self)} no client connection possible to slurm server"
            )

        url = "jobs"

        logger.debug(f"{callsign(self)} client connection seems possible for {url}")

        # Talk to the slurmrestd server.
        response = await self.client_get(url)

        if "jobs" not in response:
            logger.debug(f"jobs response:\n{json.dumps(response, indent=4)}")
            raise RuntimeError("jobs response does not contain jobs field (see log)")

        # Turn the list of jobs in the response to a dict indexed by job_id.
        jobs_dict = {}
        for job in response["jobs"]:
            jobs_dict[job["job_id"]] = job

        # Look through all the jobs we are querying.
        job_info_models: Dict[int, JobSummaryModel] = {}
        for job_id in job_ids:
            # Get job entry for this job from slurm's response.
            job_entry = jobs_dict.get(job_id)

            # Slurm knows no job entry with this job_id?
            if job_entry is None:
                job_state = self.FINISHED_JOB_STATE_UNKNOWN
            else:
                job_state = job_entry.get("job_state")

            # Job's state indicates not finished?
            if job_state not in self.UNFINISHED_JOB_STATES:
                logger.debug(
                    f"[SQUJOB] {job_id} considered finished because state is {job_state}"
                )
                is_finished = True
            else:
                logger.debug(
                    f"[SQUJOB] {job_id} considered not finished because state is {job_state}"
                )
                is_finished = False

            # Make an object representing the job's info.
            job_info_model = JobSummaryModel(
                job_id=job_id,
                is_finished=is_finished,
                other=f"job_state is {job_state}",
            )

            # Add to the list to be returned.
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

        properties = copy.deepcopy(properties)

        is_client_connection_possible = await self.is_client_connection_possible()

        if not is_client_connection_possible:
            raise RuntimeError(
                f"{callsign(self)} no client connection possible to slurm server"
            )

        properties.oversubscribe = None

        submission_model = OpenapiJobSubmission(
            script=f"#!/bin/bash\nsource {script_filename}\n",
            job=properties,
            jobs=None,
        )

        submission_dict = submission_model.dict(exclude_none=True)
        submission_json = json.dumps(
            submission_dict,
            indent=4,
        )

        url = "job/submit"

        logger.debug(
            f"[SLRMSUB] {callsign(self)} client connection seems possible for {url}\n{submission_json}"
        )

        # Talk to the slurmrestd server.
        response_dict = await self.client_post(
            url, json=submission_dict, read_until_eof=False
        )

        logger.debug(
            describe(f"[SLRMSUB] {callsign(self)} job submit response", response_dict)
        )

        # Check the response.
        jsr = OpenapiJobSubmissionResponse(**response_dict)

        if jsr.errors is not None and len(jsr.errors) > 0:
            error = jsr.errors[0]
            error_number = error.error_number
            # TODO: Figure out why the 0.0.38 spec says error_number, but the server is giving error_code instead.
            if error_number is None:
                error_number = response_dict.get("errors")[0].get(
                    "error_code", "unknown"
                )
            raise Rejected(
                f"{callsign(self)} slurmrestd error {error_number}: {error.error}"
            )

        logger.debug(
            f"{callsign(self)} submitted job_id {jsr.job_id}: {jsr.job_submit_user_msg}"
        )

        return jsr.job_id  # type: ignore
