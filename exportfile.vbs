Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "exporter\test.bat"
oShell.Run strArgs, 0, false