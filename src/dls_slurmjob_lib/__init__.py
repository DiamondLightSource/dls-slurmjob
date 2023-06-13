from importlib.metadata import version

__version__ = version("dls-slurmjob")
del version

__all__ = ["__version__"]
