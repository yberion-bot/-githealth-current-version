#!/usr/bin/env python3
import subprocess, datetime, os, json
from typing import List, Tuple

def run(cmd: str, check: bool=False) -> Tuple[int,str,str]:
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    return p.returncode, (out or "").strip(), (err or "").strip()

def echo(msg: str):
    print(msg)

def now_iso():
    return datetime.datetime.now().isoformat()

def get_remotes() -> List[str]:
    rc, out, err = run("git remote")
    if rc != 0:
        raise RuntimeError(f"git remote failed: {err}")
    return [r for r in out.splitlines() if r.strip()]

def list_local_branches(patterns: List[str]=None) -> List[str]:
    rc, out, err = run("git for-each-ref --format=%(refname:short) refs/heads/")
    if rc != 0:
        raise RuntimeError(f"failed to list branches: {err}")
    branches = [b.strip() for b in out.replace('\r','').splitlines() if b.strip()]
    if not branches:
        rc, cur, _ = run("git branch --show-current")
        cur = cur.strip() if rc == 0 else None
        if cur:
            return [cur]
    if not patterns:
        return branches
    selected = []
    for b in branches:
        for p in patterns:
            if b.startswith(p):
                selected.append(b)
                break
    return selected

def branch_status(branch: str) -> dict:
    rc, out, err = run(f"git status --branch --porcelain=v2 {branch}")
    text = (out or "") + "\n" + (err or "")
    info = {
        'raw': text,
        'has_local_changes': any(line and not line.startswith('#') for line in text.splitlines()),
        'behind': 'behind' in text,
        'ahead': 'ahead' in text,
        'diverged': 'diverged' in text or ('behind' in text and 'ahead' in text)
    }
    return info

AUTO_MERGE_RULES = {
    'main': 'ours',
    'master': 'ours',
    'dev': 'theirs',
    'feature/': 'ours',
    'hotfix/': 'theirs'
}

def determine_strategy(branch: str) -> str:
    for key, pref in AUTO_MERGE_RULES.items():
        if key in branch:
            return pref
    return 'theirs'

def auto_merge(branch: str, remote: str, no_stash: bool=False) -> Tuple[bool,str]:
    strategy = determine_strategy(branch)
    echo(f"🧩 Auto-Merge-Strategie für {branch}: {strategy}")
    if not no_stash:
        run("git add -A && git stash push -m 'yberion auto-merge stash'")
    rc, out, err = run(f"git fetch {remote} {branch} && git merge -X {strategy} {remote}/{branch}")
    merged_output = (out + "\n" + err).strip()
    conflict = 'CONFLICT' in merged_output or (rc != 0 and 'error:' in merged_output.lower())
    if conflict:
        echo("⚠️ Auto-Merge hat Konflikte erzeugt — manuelle Lösung empfohlen.")
        run("git merge --abort || true")
        if not no_stash:
            run("git stash pop || true")
        return False, merged_output
    else:
        if not no_stash:
            run("git stash pop || true")
        return True, merged_output

def push_branch(branch: str, remote: str) -> Tuple[bool,str]:
    rc, out, err = run(f"git push {remote} {branch}")
    ok = rc == 0
    return ok, (out + "\n" + err).strip()

def write_html_scorecard(branch_summaries: List[dict], outname: str='yberion_githealth.html'):
    rows = ""
    for b in branch_summaries:
        rows += f"<tr><td>{b['branch']}</td><td>{'✔️' if b.get('push_success') else '❌'}</td>"
        rows += f"<td>{'⚠️' if b.get('conflict_predicted') else '✔️'}</td>"
        rows += f"<td>{b.get('pr_url') or ''}</td><td>{', '.join(b.get('notes',[]))}</td></tr>\n"
    html = f"<html><head><meta charset='utf-8'><title>Yberion GitHealth</title></head><body>"
    html += f"<h1>📊 Yberion GitHealth Scorecard</h1><p>Erstellt: {now_iso()}</p>"
    html += f"<table border='1'><tr><th>Branch</th><th>Push</th><th>Conflict</th><th>PR</th><th>Notes</th></tr>{rows}</table></body></html>"
    with open(outname,'w', encoding='utf-8') as f:
        f.write(html)
    echo(f"💾 HTML-Scorecard geschrieben: {outname}")

def manage_branches(remote: str='origin', do_push: bool=True, do_stash: bool=True, create_pr: bool=False, patterns: List[str]=None):
    echo('🔹 Yberion Multi-Branch Manager startet — ' + now_iso())
    remotes = [remote]
    try:
        remotes = get_remotes()
    except Exception as e:
        echo(f"⚠️ Fehler beim Ermitteln der Remotes: {e} — verwende default '{remote}'")
        remotes = [remote]
    echo(f"🌐 Remotes: {remotes}")
    branches = list_local_branches(patterns)
    if not branches:
        echo('⚠️ Keine Branches gefunden — Abbruch.')
        return
    echo(f"🔎 Gefundene Branches: {branches}")
    results = []
    for b in branches:
        echo(f"\n--- Verarbeitung {b} (priority 0) ---")
        # fetch per remote (Windows-safe)
        for r in remotes:
            run(f'git fetch {r}')
        # auto-merge attempt
        conflict_pred = False
        for r in remotes:
            ok, out = auto_merge(b, r, no_stash=not do_stash)
            if not ok:
                conflict_pred = True
        res = {'branch':b,'conflict_predicted':conflict_pred,'push_success':False,'notes':[]}
        if do_push:
            for r in remotes:
                ok, push_out = push_branch(b,r)
                res['push_success'] = ok
        results.append(res)
    write_html_scorecard(results)

if __name__ == '__main__':
    manage_branches()
