
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
Extension("ldap", ["ldap.pyx"]),
Extension("checker", ["checker.pyx"]),
Extension("finder", ["finder.pyx"]),
Extension("utils", ["utils.pyx"]),
]

setup(
name = 'bchecker',
cmdclass = {'build_ext': build_ext},
ext_modules = ext_modules
)