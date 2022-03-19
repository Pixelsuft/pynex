import os
import sys
import shutil
from setuptools import setup, find_packages
from pynex import __version__ as version


readme = open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read()
requirements = ['pygame', 'Pillow']
for i in sys.argv[1:]:
    if not i.lower() == 'sdist' and not i.lower() == 'bdist_wheel':
        continue
    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'build'))
    except Exception as __err:
        if __err:
            'Just for PyCharm'
    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'dist'))
    except Exception as __err:
        if __err:
            'Just for PyCharm'
    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'pynex.egg-info'))
    except Exception as __err:
        if __err:
            'Just for PyCharm'
    break


setup(
    name="pynex",
    author="Pixelsuft",
    url="https://github.com/Pixelsuft/pynex",
    project_urls={
        "Readme": "https://github.com/Pixelsuft/pynex/blob/main/README.MD",
        "Example": "https://github.com/Pixelsuft/pynex/blob/main/main.py",
        "Issue tracker": "https://github.com/Pixelsuft/pynex/issues",
    },
    version=version,
    packages=find_packages(),
    license="MIT",
    description="PyGame-based GUI Library.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
    py_modules=["pynex"],
    package_dir={'': '.'},
    keywords="pynex"
)
