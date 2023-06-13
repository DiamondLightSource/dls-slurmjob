# Can't find something.
class NotFound(RuntimeError):
    pass


# Job rejected by slurm engine, for example missing some required property.
class Rejected(RuntimeError):
    pass
