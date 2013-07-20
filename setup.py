import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-exportdata',
    version='0.2',
    license='ISC',
    description='Export model data (with selected fields) to csv file',
    long_description=read('README.md') + read('CHANGES.md'),
    keywords='django export import data csv json file dumpdata',
    url='https://github.com/saippuakauppias/django-exportdata',
    author='Denis Veselov',
    author_email='progr.mail@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'django'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
)
