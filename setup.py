from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='muddy',
    version='2019.7.21-2',
    author='Lucas Estienne, Daniel Innes',
    author_email='lucas@estienne.sh; daniel.w.innes@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=7,<8',
        'overload>=1.1'
    ],
    entry_points='''
        [console_scripts]
        muddy=muddy.scripts.mudcli:cli
    ''',
    url="https://github.com/lstn/muddy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)