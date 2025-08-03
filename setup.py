from setuptools import setup, find_packages

setup(
    name="taskgen",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taskgen = taskgen.cli:main'
        ]
    },
    install_requires=[ ],
)