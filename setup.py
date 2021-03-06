import setuptools
import fludo

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fludo',
    version=fludo.version,
    author='Zsolt Nagy',
    author_email='nazsolti@outlook.com',
    description='A lightweight e-liquid calculator package for Python 3.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/antariandel/fludo',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
