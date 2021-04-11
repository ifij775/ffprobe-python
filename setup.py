#!/usr/bin/env python

from setuptools import setup
# from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ffprobe-python',
    version='2.0.0',
    description="""
    A wrapper around ffprobe command to extract metadata from media files.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Chris Weed',
    author_email='chrisweed@gmail.com',
    maintainer='Chris Weed',
    maintainer_email='chrisweed@gmail.com',
    url='https://github.com/ifij775/ffprobe-python',
    packages=['ffprobe'],
    keywords='ffmpeg, ffprobe, mpeg, mp4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries'
    ])
