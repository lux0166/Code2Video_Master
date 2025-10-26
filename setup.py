from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="Code2Video",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'gui_scripts': [
            'code2video = src.gui:main',
        ],
    },
)
