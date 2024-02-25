@echo off

set conda_environment=StardistForImagej
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\ImageJSoftware\AutomaticCountingWithRoiatlas\AutomaticCounting\Initial_File.py" 
call %conda_path%\Scripts\deactivate




