0<0# : ^
''' 
@echo off
python "%~f0" %*
exit /b 0
'''
import sys
from harmony_model_checker.main import main

if __name__ == "__main__":
    sys.exit(main())
