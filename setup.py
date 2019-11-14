# from distutils.core import setup
from setuptools import setup, find_packages


setup(
    name='cyapi',
    version='0.9.12',
    packages=find_packages(),
    license='GNU',
    long_description=open('README.md').read(),
    package_data={'cyapi': ['reqs/*.json', 'exclusions/*.json']},
    install_requires=[
        'pyjwt',
        'requests',
        'python-dateutil',
        'pytz',
        'tqdm'
    ],
    extras_require={
        ':python_version == "2.7"': [
            'futures',
        ]
    }
)

