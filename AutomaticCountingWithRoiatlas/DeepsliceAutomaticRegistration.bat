@echo off

set conda_environment=DeepSlice
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\ImageJSoftware\DeepsliceAutomaticAtlasRegistration\Application\Application\Application.py" 
call %conda_path%\Scripts\deactivate




