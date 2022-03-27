from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.annotate = True

setup(
    ext_modules=cythonize("ProblemACython.pyx")
)
