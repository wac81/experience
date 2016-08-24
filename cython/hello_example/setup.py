'''
you can run:
python setup.py build_ext -i
complie py to so or pyd
'''

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("hello", ["hello.py"])]

setup(
name = 'Hello world app',
cmdclass = {'build_ext': build_ext},
ext_modules = ext_modules
)