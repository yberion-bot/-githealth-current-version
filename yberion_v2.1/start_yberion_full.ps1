<#
.SYNOPSIS
    Startet Yberion v2.1 vollständig in Schwellenhütermodus mit aktivierten Junior- und Senior-Agenten.
.DESCRIPTION
    - Activator BAT ausführen
    - Python Launcher korrekt starten
    - Junior-Agent: Autocue, WebResearch, Audit aktiv
    - Schwellenhütermodus aktiv
#>

# Wechsel ins Yberion v2.1-Verzeichnis
cd "C:\Users\schat\yberion\smart_commit_export\yberion_v2.1"

# Korrigierter Pfad zu Python
$pythonPath = "C:\Users\schat\AppData\Local\Programs\Python\Python314\python.exe"

if (-Not (Test-Path $pythonPath)) {
    Write-Host "Python nicht gefunden unter $pythonPath"
    exit
}

# Activator starten (mit korrektem Pfad)
Write-Host "Starte Yberion Activator..."
Start-Process -FilePath ".\yberion_activator.bat" -Wait

# Launcher-Pfad prüfen
$launcherPath = ".\src\yberion_live_launcher.py"
if (-Not (Test-Path $launcherPath)) {
    Write-Host "Launcher-Datei nicht gefunden unter $launcherPath"
    exit
}

# Yberion vollständig hochfahren
Write-Host "Starte Yberion Launcher im Schwellenhütermodus..."
& "$pythonPath" "$launcherPath" --mode "schwellenhüter" --junior-autocue on --web-research on --audit on

Write-Host "✅ Yberion v2.1 ist nun voll operational. Junior + Senior Agent aktiv."
