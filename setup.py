import os
import setuptools  # type: ignore

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "VERSION")) as f:
    version = f.read().strip()

setuptools.setup(
    name="openvpn-api",
    version=version,
    description="A Python API for the OpenVPN management interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jamie-/openvpn-api",
    author="Jamie Scott",
    author_email="contact@jami.org.uk",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="openvpn monitor management",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    install_requires=["netaddr", "openvpn_status",],
    project_urls={
        "Source": "https://github.com/Jamie-/openvpn-api",
        "Bug Reports": "https://github.com/Jamie-/openvpn-api/issues",
    },
)
