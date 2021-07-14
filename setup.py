from setuptools import setup, find_packages

setup(
    name='allen-py-client',
    version='1.1.101',
    description='Unofficial python wrapper for Allen\'s web API.',
    long_description=open('README.rst', encoding="utf8").read(),
    author='Harsh Patil',
    author_email='ifung230@gmail.com',
    url='https://github.com/lamergameryt/allen-py-client',
    download_url='https://github.com/lamergameryt/allen-py-client',
    keywords=['python', 'allen'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=['requests', 'termcolor', 'stdiomask'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'allen=allen.command_line:main'
        ]
    }
)
