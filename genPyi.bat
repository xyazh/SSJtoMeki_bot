@echo off
rem 生成 xyacqbot 的类型存根（需要先 pip install mypy）
set "PYTHONPATH=%~dp0"
stubgen -p xyacqbot -o stubs