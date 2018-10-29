import subprocess
import sys
import setuptools
from arnoldc.__version__ import VERSION


if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="arnoldc",
        version=VERSION,
        author="Corey McCandless",
        author_email="crm1994@gmail.com",
        description=(
            "Python implementation of ArnoldC"
        ),
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/cmccandless/arnoldc",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        entry_points={
            'console_scripts': [
                'arnoldc = arnoldc.__main__:main'
            ],
        },
        install_requires=[],
        include_package_data=True,
        python_requires='>=3.5.2',
    )
