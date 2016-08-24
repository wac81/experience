#coding=utf8
from distutils.core import setup
from Cython.Build import cythonize
#cythonize：编译源代码为C或C++，返回一个distutils Extension对象列表
setup(ext_modules=cythonize('fib.pyx'))