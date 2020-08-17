Get-ChildItem "Files" -Directory | Get-ChildItem -attributes hidden | Remove-Item -Verbose -Recurse -Force
