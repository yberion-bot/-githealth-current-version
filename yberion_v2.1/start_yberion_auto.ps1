<#
.SYNOPSIS
    Startet Yberion v2.1 vollständig in Schwellenhütermodus mit aktivierten Junior- und Senior-Agenten.
.DESCRIPTION
    - Prüft automatisch den Python-Pfad
    - Findet den Yberion Launcher
    - Aktiviert Junior-Agent (Autocue/WebResearch/Audit)
    - Startet Senior-Agent für konvergente Synthese
    - Aktiviert Schwellenhütermodus
#>

# Wechsel ins Yberion v2.1-Verzeichnis
$baseDir = "C:\Users\schat\yberion\smart_commit_export"
$yberionDirs = @("yberion_v2.1", "yberion-2.1\src")

# Python-Pfad automatisch suchen
$pythonPath = Get-Command python | Select-Object -ExpandProperty Source
if (-not $pythonPath) {
    Write-Host "Python konnte nicht gefunden werden. Bitte Pfad manuell prüfen."
    exit
}
Write-Host "✅ Python gefunden unter $pythonPath"

# Launcher automatisch suchen
$launcherPath = $null
foreach ($dir in $yberionDirs) {
    $candidate = Join-Path $baseDir $dir
    $candidateLauncher = Join-Path $candidate "yberion_live_launcher.py"
    if (Test-Path $candidateLauncher) {
        $launcherPath = $candidateLauncher
        break
    }
}

if (-not $launcherPath) {
    Write-Host "❌ Yberion Launcher nicht gefunden. Bitte Pfad prüfen."
    exit
}
Write-Host "✅ Launcher gefunden unter $launcherPath"

# Activator starten
$activatorPath = Join-Path $baseDir "yberion_v2.1\yberion_activator.bat"
if (Test-Path $activatorPath) {
    Write-Host "Starte Yberion Activator..."
    Start-Process -FilePath $activatorPath -Wait
} else {
    Write-Host "⚠ Activator BAT nicht gefunden, überspringe Activator Schritt."
}

# Yberion starten
Write-Host "Starte Yberion im Schwellenhütermodus mit Junior/Senior-Agent..."
& "$pythonPath" "$launcherPath" --mode "schwellenhüter" --junior-autocue on --web-research on --audit on

Write-Host "✅ Yberion v2.1 ist nun voll operational. Junior + Senior Agent aktiv."
