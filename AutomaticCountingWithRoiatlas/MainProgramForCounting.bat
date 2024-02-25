@echo off
::call activate [base]
:: cmd/k prevent to close bat file
python "X:\Users\LabSoftware\ImageJSoftware\AutomaticCountingWithRoiatlas\ManagerCountingCells\ManagerCountingCells\MainProgramForCountingCells.py" > output.txt


timeout /t 5 /nobreak >nul

:: Read content of output.txt into a variable using for /f
for /f "delims=" %%a in (output.txt) do set "pythonOutput=%%a"

:: Display Python script output
echo Python script output: %pythonOutput%

:: Check if pythonOutput is equal to 3
if "%pythonOutput%" equ "3" (
    echo Running another Python script...
    call AutomaticCounting.bat
	)else if "%pythonOutput%" equ "1"  (
	    echo Running another Python script...
        call DeepsliceAutomaticRegistration.bat
) else (
    echo pythonOutput is not 3. No need to run another script.
)



:: Check if pythonOutput is 3
   
pause
:: call  