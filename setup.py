import os
import codecs
from setuptools import setup, find_packages
import flipper

basedir = os.path.dirname(os.path.abspath(__file__))

requirements_file = os.path.join(basedir, 'requirements.txt')
with open(requirements_file, encoding='utf8') as f:
    install_requires = [line.rstrip() for line in f.readlines()]

extras_require = {}

tests_require = [
    'pytest',
]


def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name='flipper',
    version=flipper.__version__,
    description=flipper.__doc__.strip(),
    long_description=long_description(),
    url='',
    download_url='https://github.com/yukinarit/flipper',
    author=flipper.__author__,
    author_email='yukinarit84@gmail.com',
    license=flipper.__licence__,
    entry_points={
        'console_scripts': [
            'flipper=flipper.__main__:main',
        ],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        #'Topic :: Internet :: WWW/HTTP',
    ],

    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_require,
    packages=find_packages(),
)
