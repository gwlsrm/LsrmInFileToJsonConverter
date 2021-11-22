@echo off
for /R %%i in (*.?in) do infile_to_json.py "%%i"