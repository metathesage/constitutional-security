#!/usr/bin/env python3
"""
Setup script for Constitutional Security repository.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="constitutional-security",
    version="1.0.0",
    author="Michael A. Scott (metathesage)",
    author_email="dev@pnthr.xyz",
    description="Constitutional Security: Provably Safe AI Deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metathesage/constitutional-security",
    project_urls={
        "Paper": "https://pnthr.xyz/research/constitutional-security",
        "arXiv": "https://arxiv.org/abs/2611.XXXXX",
        "Issues": "https://github.com/metathesage/constitutional-security/issues",
    },
    packages=find_packages(where="."),
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24",
        "pandas>=2.0",
        "pydantic>=2.0",
        "pyyaml>=6.0",
        "lark>=1.1",
        "tqdm>=4.66",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4",
            "black>=23.0",
            "ruff>=0.1",
            "mypy>=1.0",
            "pre-commit>=3.0",
        ],
        "verification": [
            "z3-solver>=4.12",
            "pysmt>=0.9",
        ],
        "benchmarks": [
            "torch>=2.0",
            "transformers>=4.30",
            "accelerate>=0.20",
        ],
    },
    entry_points={
        "console_scripts": [
            "cs-verify=verification.cli:main",
            "cs-benchmark=benchmarks.benchmarks:main",
            "cs-build-paper=scripts.build_pdf:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Rust",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "Topic :: Software Development :: Verification",
    ],
    include_package_data=True,
    package_data={
        "psl": ["examples/*.psl", "grammar.lark"],
        "verification": ["domains/*.json"],
        "docs": ["*.md"],
    },
)