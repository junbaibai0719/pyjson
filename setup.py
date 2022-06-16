from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension("pyjson", ["pyjson.py"])
]

setup(
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
