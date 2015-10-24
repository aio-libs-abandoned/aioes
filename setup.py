import os
import re
import sys
from setuptools import setup, find_packages


install_requires = ['aiohttp>=0.17.0']

PY_VER = sys.version_info

if PY_VER >= (3, 4):
    pass
elif PY_VER >= (3, 3):
    raise RuntimeError("aioes doesn't suppport Python earlier than 3.4")


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'aioes', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in aioes/__init__.py')

classifiers = [
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Environment :: Web Environment',
    'Development Status :: 4 - Beta',
    'Topic :: Database',
    'Topic :: Database :: Front-Ends',
]


setup(name='aioes',
      version=read_version(),
      description=('Elasticsearch integration with asyncio.'),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=classifiers,
      platforms=['POSIX'],
      author='Andrew Svetlov',
      author_email='andrew.svetlov@gmail.com',
      url='http://aioes.readthedocs.org',
      download_url='https://pypi.python.org/pypi/aioes',
      license='Apache 2',
      packages=find_packages(),
      install_requires=install_requires,
      include_package_data=True)
