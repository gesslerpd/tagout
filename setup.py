from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md')) as fd:
    readme = fd.read()

setup(
    name='tagout',
    version='1.0.0',
    description='A small, pythonic, HTML/XML writer',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/gesslerpd/tagout',
    author='gesslerpd',
    author_email='gesslerpd@users.noreply.github.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='tags tag html xml generator writer stream',
    packages=['tagout'],
    install_requires=(
    ),
)
