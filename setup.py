"""
Setup script for Tikun Olam - An Ethical Reasoning Architecture for AI Decision Systems
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="tikun-olam",
    version="1.0.0",
    author="Tikun Olam Contributors",
    description="An Ethical Reasoning Architecture for AI Decision Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tikun-olam",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/tikun-olam/issues",
        "Documentation": "https://tikun-olam.readthedocs.io",
        "Source Code": "https://github.com/yourusername/tikun-olam",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "google-generativeai>=0.3.0",
        "anthropic>=0.8.0",
        "openai>=1.10.0",
        "httpx>=0.26.0",
        "aiohttp>=3.9.0",
        "orjson>=3.9.0",
        "pyyaml>=6.0.1",
        "structlog>=24.1.0",
        "python-json-logger>=2.0.7",
        "python-dateutil>=2.8.2",
        "tenacity>=8.2.3",
        "jsonschema>=4.20.0",
    ],
    extras_require={
        "api": [
            "fastapi>=0.109.0",
            "uvicorn[standard]>=0.27.0",
        ],
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tikun=tikun.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
