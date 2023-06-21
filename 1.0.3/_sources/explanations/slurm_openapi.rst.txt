OPENAPI
=======================================================================

The slurmrestd server claims to conform to OpenAPI.

To turn the OpenAPI schemas into pydantic models do these steps::

    $ export SLURM_JWT=<your token>
    $ curl -s -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} -H "Content-Type: application/json" -X GET https://slurm-rest.diamond.ac.uk:8443/openapi/ > src/dls_slurmjob_api/models/openapi/openapi.json
    $ pip install datamodel-code-generator
    $ datamodel-codegen --input src/dls_slurmjob_api/models/openapi/openapi.json --input-file-type=openapi --force-optional --target-python-version=3.10 --output src/dls_slurmjob_api/models/openapi

Then you can import the models you want like::

    from dls_slurmjob_api.models.openapi.v0.field_0 import Field38JobProperties as OpenapiJobProperties

I'm not exactly sure the best way to insulate the code from having to know too much about the OpenAPI version.

You can try these curls::

    $ curl -s -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} -H "Content-Type: application/json" -X POST https://slurm-rest.diamond.ac.uk:8443/slurm/v0.0.38/job/submit -d@tests/scripts/hello1.json -v
    $ curl -s -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} -H "Content-Type: application/json" -X POST https://slurm-rest.diamond.ac.uk:8443/slurm/v0.0.38/job/submit -d@tests/scripts/hello2.json -v

sbatch tests/scripts/mib_convert1.sh

Some references
- OpenAPI Specification https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#data-types
- datamodel-code-generator https://koxudaxi.github.io/datamodel-code-generator/
- Pydantic's section on Code Generation https://docs.pydantic.dev/latest/datamodel_code_generator/
- Slurm's Specification https://slurm.schedmd.com/rest_api.html
    