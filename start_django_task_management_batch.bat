@echo off
setlocal enabledelayedexpansion

set "batch_dir=%~dp0"
set "venv_path=%batch_dir%django_task_management_venv"
echo %venv_path%
call "%venv_path%\Scripts\activate"

cd /d %batch_dir%\django_task_management
code %batch_dir%\django_task_management
call deactivate