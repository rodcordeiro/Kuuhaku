mkdir temp
$Files = @(
    ".\src\*",
    ".\.env",
    ".\requirements.txt"
)
$Exclude = @()

Copy-item $Files -Destination .\temp -Exclude $Exclude -Recurse
# Copy-item .\.env -Destination .\temp 
# Copy-item .\requirements.txt -Destination .\temp 
Compress-Archive -Path .\temp\* -DestinationPath .\app.zip -Force
Remove-Item -Path .\temp -Recurse -Force
