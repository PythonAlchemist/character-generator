from setuptools import setup, find_packages

# Define project details
project_name = "char-gen"
version = "0.1.0"
description = "Character Generator Project"
author = "PythonAlchemist"
url = "https://github.com/PythonAlchemist/character-generator"

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Setup configuration
setup(
    name=project_name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    url=url,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add your dependencies here
    ],
)
