try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

__version__ = '0.3.0'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='amplot',
    packages=['amplot'],
    version=__version__,
    description='A map plot based on Amap(高德地图).',
    long_description=read('README.md'),
    author='Yang Bai',
    author_email='by66666@gmail.com',
    url='https://github.com/KECB/amplot',
    download_url='',
    keywords=['amplot', 'map', 'plot'],
    classifiers=[],
    license='MIT',
    install_requires=['requests'],
)
