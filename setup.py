'''
Created on 2018-12-10

@author: feixu@iflytek.com
'''
from setuptools import setup, find_packages

setup(name='IflyTool',
      version='0.0.1',
      description='IflyTool',
      author='feixu',
      author_email='feixu@iflytek.com',
      package_dir = {'': 'lib'},
      packages = find_packages(where = "lib")
     )