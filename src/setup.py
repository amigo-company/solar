import os
import shutil
from setuptools import setup, find_packages

setup(
    name='solar',
    author='Daniel Ervilha',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
)

def move_to_pkg(src: str):
    tgt = f"../pkg/{src}"
    if os.path.exists(tgt):
        shutil.rmtree(tgt)
    shutil.move(src, tgt)

move_to_pkg("build")
move_to_pkg("dist")
move_to_pkg("solar.egg-info")
