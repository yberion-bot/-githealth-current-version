# pip install GitPython
import git
import datetime
import os

# Pfad zu deinem lokalen Repo
repo_path = r"C:\Users\schat\yberion"
repo = git.Repo(repo_path)

# Alle Änderungen hinzufügen
repo.git.add(all=True)

# Commit mit Zeitstempel
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
repo.index.commit(f"Auto-Update {ts}")

# Remote push (SSH muss vorher eingerichtet sein)
origin = repo.remote(name="origin")
origin.push()
print(f"[Yberion] ✅ Push completed at {ts}")
