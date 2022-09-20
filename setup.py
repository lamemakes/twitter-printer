from setuptools import setup
import pilot_drive

import twitter_printer

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="twitter-printer",
    version=twitter_printer.__version__,
    author="Wesley Appler",
    author_email="wes@lamemakes.com",
    description="The Twitter Printer materializes anything you tweet at it utilizing some Python & an old receipt printer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamemakes/twitter-printer",
    project_urls={
        "Bug Tracker": "https://github.com/lamemakes/twitter-printer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    install_requires=["python-escpos", "twint", "Pillow"],
    packages=["twitter_printer"],
    package_dir={'twitter-printer': 'twitter_printer'},
    include_package_data=True,
    python_requires=">=3.6",
)
