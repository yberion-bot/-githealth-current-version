\# Yberion — Installer Build



Automatischer Build: Bei jedem `git push` auf `main` erzeugt die GitHub Actions einen Windows Installer.

Artefakte findest du in Actions → Workflow run → Artifacts.



Lokal bauen:

1\. Installiere Python 3.11+, PyInstaller, Inno Setup.

2\. Passe ggf. `ENTRY\\\_POINT` in `build.bat` an.

3\. Doppelklick `build.bat` → erzeugt `Yberion\\\_installer\\\_2.1.exe`.



Portable SFX: siehe `make\\\_sfx.bat`.

