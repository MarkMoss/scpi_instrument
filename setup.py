import setuptools

setuptools.setup(
    name="scpi_instrument",
    version="0.0.4", 
    author="Mark Moss",
    author_email="scpi@mmoss.org",
    desciption="A package to map SCPI commands to Python objects.",
    packages=setuptools.find_packages(),
    install_requires=['PyVISA'],
    python_requires=">=2.7")