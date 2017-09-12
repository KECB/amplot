try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.2'
setup(
    name='amplot',
    packages=['amplot'],
    version=version,
    description='A map plot based on Amap(高德地图).',
    author='Yang Bai',
    author_email='by66666@gmail.com',
    url='https://github.com/KECB/amplot',
    download_url='https://github.com/KECB/amplot/archive/0.1.tar.gz',
    keywords=['amplot', 'map', 'plot'],
    classifiers=[],
)
