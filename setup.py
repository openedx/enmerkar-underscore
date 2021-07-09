#!/usr/bin/env python
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '2.1.0'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip() for line in open(path).readlines()
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return not (
        line == '' or
        line.startswith('-r') or
        line.startswith('#') or
        line.startswith('-e') or
        line.startswith('git+') or
        line.startswith('-c')
    )


setup(
    name='enmerkar-underscore',
    version=version,
    description='Implements a underscore extractor for django-babel.',
    long_description=read('README.rst') + '\n\n' + read('HISTORY.rst'),
    author='edX',
    author_email='oscm@edx.org',
    url='https://github.com/edx/enmerkar-underscore',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    tests_require=load_requirements('requirements/test.in'),
    install_requires=load_requirements('requirements/base.in'),
    entry_points="""
    [babel.extractors]
    underscore = enmerkar_underscore:extract
    """,
    zip_safe=False,
    license='BSD',
    keywords='enmerkar-underscore',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',        
        'Framework :: Django :: 3.2',
    ],
)
