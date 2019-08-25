import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="johnclayton",
    version="0.0.1",
    author="John Clayton",
    author_email="johnclayton72@gmail.com",
    description="A program to ensure the HDMI/monitor connection wakes up when movement is detected via an IR sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johncclayton/wakeup.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Raspberry Pi",
    ],
)