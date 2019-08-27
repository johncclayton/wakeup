import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wakeup",
    version="0.0.1",
    author="John Clayton",
    author_email="johnclayton72@gmail.com",
    description="A suite of programs to monitor an IR sensor and then turn on an HDMI/monitor when movement is detected.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johncclayton/wakeup.git",
    packages=setuptools.find_packages(),
    install_requires = [
        'rpi.gpio==0.7.0',
        'pigpio==1.44',
        'gpiozero==1.5.1',
        'prometheus_client==0.7.1',
        'pyzmq==18.1.0',
    ],
    scripts = [
        'wakeup/screen_on.sh'
    ],
    entry_points={
        'console_scripts': [
            'motion_hdmi = wakeup.motion_hdmi_service:main_func',
            'motion_pub = wakeup.motion_pub_service:main_func',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Raspberry Pi",
    ],
)