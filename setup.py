import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="miniipe",
    version="0.1.8",
    author="Thomas van Dijk",
    author_email="tvdmaps@gmail.com",
    description="An easy, no-dependencies package for writing IPE files from Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tcvdijk/mini-ipe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
