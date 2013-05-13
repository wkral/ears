"""
Ears will listen for file changes from your editor and execute actions for you.
"""
from setuptools import find_packages, setup

setup(
    name = "ears",
    version = "0.1",

    author = "William Kral",
    author_email = "william.kral@gmail.com",
    license = "BSD",
    description = __doc__,
    long_description = open("README.md").read(),
    url = "https://github.com/wkral/ears",

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML"
    ],

    packages = find_packages(),
    scripts = ['scripts/ears'],


    include_package_data = True,
    zip_safe = False,
    )
