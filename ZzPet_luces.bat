@echo off
title Launcher ZzPet Luces

echo Iniciando ZzPet Luces...

REM Obtener la ruta del directorio actual
set ROOT_DIR=%~dp0

start "ZzPet Luces - Traductor" /d "%ROOT_DIR%" cmd /k "python traductor.py"
start "ZzPet Luces - MCP Pipe" /d "%ROOT_DIR%mcp-calculator" cmd /k "python mcp_pipe.py"

echo Procesos lanzados con exito.
