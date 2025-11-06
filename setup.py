"""Setup configuration for ScienceSheetForge"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sciencesheetforge",
    version="2.0.0",
    author="Charles Martin",
    author_email="charlesmartinedd@github.com",
    description="AI-Powered Science Worksheet Generator for K-8 Educators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/charlesmartinedd/ScienceSheetForge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "bandit>=1.7.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "sciencesheetforge=app:main",
        ],
    },
)
