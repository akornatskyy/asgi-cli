import re

from setuptools import setup

README = open("README.md").read()
VERSION = (
    re.search(
        r"__version__ = \"(.+)\"", open("src/asgi_cli/__init__.py").read()
    )
    .group(1)
    .strip()
)

setup(
    name="asgi-cli",
    version=VERSION,
    python_requires=">=3.6",
    description="Call ASGI Python application from command line,"
    " just like CURL",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/akornatskyy/asgi-cli",
    author="Andriy Kornatskyy",
    author_email="andriy.kornatskyy@live.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="",
    packages=["asgi_cli"],
    package_data={"asgi_cli": ["py.typed"]},
    package_dir={"": "src"},
    zip_safe=True,
    install_requires=[],
    entry_points={"console_scripts": ["asgi-cli=asgi_cli.main:main"]},
    platforms="any",
)
