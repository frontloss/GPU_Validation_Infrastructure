start /wait setx PATH "C:\Python38;%CD%\bin"
start /wait setx PYTHONPATH "%CD%;%CD%\Libs;%CD%\bin"
start /wait bcdedit -set TESTSIGNING ON