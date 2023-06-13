import json
from typing import Optional

from pydantic import BaseModel


class JobSummaryModel(BaseModel):
    """
    Model containing job info.
    """

    job_id: int

    # True/False if job is finished, None if not started or otherwise unknown.
    is_finished: Optional[bool] = None

    # Any other info in human readable form that the slurmer can provide?
    other: Optional[str] = None

    def serialize(self):
        """Serialize the launch info for storing in a persistent database."""
        return json.dumps(self.dict())
