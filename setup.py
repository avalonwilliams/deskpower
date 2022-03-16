import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="deskpower",
    version="1.0",
    description="UPower event listener for shell scripting",
    long_description=read("README.md"),
    license="GPLv3+",
    author="Avalon Williams",
    author_email="avalonwilliams@protonmail.com",
    packages=["deskpower"],
    install_requires=["pydbus", "pygobject"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Desktop Environment",
        "Topic :: System :: Power (UPS)",
        "Topic :: System :: Monitoring"
    ],
    entry_points = {
        "console_scripts": [
            "deskpower = deskpower.deskpower:main"
        ]
    },
)
