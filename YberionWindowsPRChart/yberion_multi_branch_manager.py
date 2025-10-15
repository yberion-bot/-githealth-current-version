#!/usr/bin/env python3
import subprocess, datetime, os, json, webbrowser
from typing import List, Tuple
import plotly.graph_objects as go

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

def create_pr(branch: str, remote: str='origin') -> str:
    import os, requests
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return ""
    rc, out, err = run("git remote get-url " + remote)
    if rc != 0: return ""
    url = out.strip()
    if url.endswith(".git"): url = url[:-4]
    if url.startswith("git@github.com:"): url = "https://api.github.com/repos/" + url[15:]
    elif url.startswith("https://github.com/"): url = "https://api.github.com/repos/" + url[19:]
    api_url = url + "/pulls"
    headers = {"Authorization": f"token {token}"}
    data = {"title": f"Automated PR: {branch}", "head": branch, "base": "main"}
    r = requests.post(api_url, headers=headers, json=data)
    if r.status_code == 201:
        return r.json().get('html_url',"")
    return ""

def write_html_scorecard(branch_summaries: List[dict], outname: str='yberion_githealth.html'):
    rows = ""
    push_vals, conflict_vals = [], []
    for b in branch_summaries:
        rows += f"<tr><td>{b['branch']}</td><td>{'✔️' if b.get('push_success') else '❌'}</td>"
        rows += f"<td>{'⚠️' if b.get('conflict_predicted') else '✔️'}</td>"
        rows += f"<td>{b.get('pr_url') or ''}</td><td>{', '.join(b.get('notes',[]))}</td></tr>\n"
        push_vals.append(1 if b.get('push_success') else 0)
        conflict_vals.append(1 if b.get('conflict_predicted') else 0)
    html = f"<html><head><meta charset='utf-8'><title>Yberion GitHealth</title></head><body>"
    html += f"<h1>📊 Yberion GitHealth Scorecard</h1><p>Erstellt: {now_iso()}</p>"
    html += f"<table border='1'><tr><th>Branch</th><th>Push</th><th>Conflict</th><th>PR</th><th>Notes</th></tr>{rows}</table>"
    # Add chart
    fig = go.Figure(data=[go.Bar(name='Push Success', x=[b['branch'] for b in branch_summaries], y=push_vals),
                           go.Bar(name='Conflict', x=[b['branch'] for b in branch_summaries], y=conflict_vals)])
    fig.update_layout(barmode='group', title_text='Yberion GitHealth Visual Summary')
    chart_file = outname.replace(".html","_chart.html")
    fig.write_html(chart_file)
    html += f"<p>📊 <a href='{chart_file}'>View interactive chart</a></p>"
    html += "</body></html>"
    with open(outname,'w', encoding='utf-8') as f:
        f.write(html)
    echo(f"💾 HTML-Scorecard geschrieben: {outname}")

def manage_branches(remote: str='origin', do_push: bool=True, do_stash: bool=True, create_pr_flag: bool=False, patterns: List[str]=None):
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
        # fetch per remote
        for r in remotes:
            run(f'git fetch {r}')
        conflict_pred = False
        for r in remotes:
            ok, out = auto_merge(b, r, no_stash=not do_stash)
            if not ok: conflict_pred = True
        pr_url = create_pr(b, remotes[0]) if create_pr_flag else ""
        res = {'branch':b,'conflict_predicted':conflict_pred,'push_success':False,'pr_url':pr_url,'notes':[]}
        if do_push:
            for r in remotes:
                ok, push_out = push_branch(b,r)
                res['push_success'] = ok
        results.append(res)
    write_html_scorecard(results)

if __name__ == '__main__':
    import sys
    create_pr_flag = '--create-pr' in sys.argv
    manage_branches(create_pr_flag=create_pr_flag)
