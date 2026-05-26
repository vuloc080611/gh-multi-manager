
### 3. `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name="gh-multi-manager",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.0",
        "PyGithub>=2.1.0",
        "GitPython>=3.1.30",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "gh-multi=gh_multi.cli:cli",
        ],
    },
    python_requires=">=3.9",
    author="Your Name",
    author_email="your@email.com",
    description="Massively manage multiple GitHub repositories from CLI",
    license="MIT",
)
