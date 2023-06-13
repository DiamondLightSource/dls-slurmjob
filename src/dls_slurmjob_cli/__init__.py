from importlib.metadata import version

__version__ = version("dls_slurmjob")
del version

__all__ = ["__version__"]
