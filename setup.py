#!/usr/bin/env python
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'sereh', '__version__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__description__'],
      url=about['__url__'],
      author='Majid Hajiloo',
      author_email='majid.hajiloo@gmail.com',
      license='MIT',
      packages=['sereh'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Multimedia :: Video',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      entry_points={
          'console_scripts': ['sereh=sereh.commandline:main'],
      },
      install_requires=[
          'chardet>=3.0.0,<4.0.0',
          'pathlib2>=2.3.0,<3.0.0;python_version<"3.4"',
      ],
      zip_safe=False)
