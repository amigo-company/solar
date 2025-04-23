@echo off
cd src/
python setup.py sdist bdist_wheel

cd ..
echo Installing package...
pip install pkg/dist/solar-0.1-py3-none-any.whl --force-reinstall
