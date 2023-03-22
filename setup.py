from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tblg",
    version="0.1.0",
    description="A command-line tool to genotype Mycobacterium tuberculosis lineage from a VCF file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbespiatykh/tblg",
    author="Dmitry Bespiatykh",
    author_email="d.bespiatykh@gmail.com",
    license="MIT",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"tblg.data": ["*.tsv"]},
    entry_points={"console_scripts": ["tblg = tblg.__main__:main"]},
    install_requires=[
        "click==8.0.4",
        "numpy==1.23.5",
        "pandas==1.5.0",
        "tabulate==0.9.0",
        "tqdm==4.64.1",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
