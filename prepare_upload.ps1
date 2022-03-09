mkdir temp
Copy-item .\src -Destination .\temp -Exclude "*\__pycache__" -Recurse
Copy-item .\.env -Destination .\temp 
Copy-item .\requirements.txt -Destination .\temp 
Compress-Archive -Path .\temp\* -DestinationPath .\app.zip -Force
Remove-Item -Path .\temp -Recurse -Force
