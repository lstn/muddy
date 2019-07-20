from setuptools import setup, find_packages

setup(
    name='muddy',
    version='2019.7.20',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        muddy=muddy.scripts.mudcli:cli
    ''',
)