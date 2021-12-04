0<0# : ^
''' 
@echo off
python "%~f0" %*
exit /b 0
'''
import sys
import app

if __name__ == "__main__":
    sys.exit(app.main())
