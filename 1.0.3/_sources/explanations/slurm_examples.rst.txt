Slurm examples
=======================================================================

Here are some slurm commands for submitting and checking jobs::

    $ export SLURM_JWT=<your token>
    $ curl -s -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} -H "Content-Type: application/json" -X POST https://slurm-rest.diamond.ac.uk:8443/slurm/v0.0.38/job/submit -d@tests/scripts/hello1.json -v
    $ curl -s -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} -H "Content-Type: application/json" -X POST https://slurm-rest.diamond.ac.uk:8443/slurm/v0.0.38/job/submit -d@tests/scripts/hello2.json -v
    $ curl -s -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} -H "Content-Type: application/json" -X POST https://slurm-rest.diamond.ac.uk:8443/slurm/v0.0.38/job/submit -d@tests/scripts/mib_convert1.json -v

Using sbatch:
    $ sbatch tests/scripts/mib_convert1.sh

To see the slurm output, if not redirected with sbatch command line or json properties::
    $ cat slurm-<job-id>.out

To check jobs running or recently ran::
    $ squeue -j <job-id>

To check jobs which ran historically::
    $ sacct -j <job-id>


