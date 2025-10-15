# Yberion Architecture — Modular Blueprint (Draft)

## Überblick
Dieses Dokument beschreibt eine modulare Architektur für **Yberion** — ein selbst‑organisierendes, Multi‑Agent‑System (MAS) mit autonomen Subagenten (Senior, Junior, Autoupdater, Git‑Agent etc.), Sicherheitsbarrieren und einem menschzentrierten Kontroll‑/Dashboard‑Layer.

Ziel: Eine robuste, sichere und nachvollziehbare Blaupause, die Autonomie, Selbstadaptation und Auditierbarkeit verbindet, ohne die Kontrolle des Host‑Operators zu gefährden.

---

## Designprinzipien
- **Minimal-Privilege**: Jeder Agent erhält genau die Rechte, die er braucht — nicht mehr.
- **Defensive Autonomie**: Agenten handeln autonom, aber unter Beobachtung (Sentinel/ Supervisor).
- **Verifizierbare Kommunikation**: Nachrichten signiert; kanalverschlüsselung.
- **Quarantäne & Rollback**: Jede riskante Aktion ist reversibel oder kann isoliert werden.
- **Auditierbarkeit**: Unveränderliche Logs, Versionshistorie und nachvollziehbare Aktionen.
- **Graceful Degradation**: Bei Ressourcenknappheit drosseln Agents ihre Aktivität statt komplett zu versagen.

---

## Kernkomponenten

### 1) Senior Agent (Stabilisator)
- Rolle: Finaler Output‑Formater, policy enforcer, human‑readable result formatter.
- Rechte: Lesender Zugriff auf Arbeitsareas, Ausführen von Review‑Funktionen, kein direkter Git‑Push.
- Verhalten: Validiert und annotiert Junior‑Ausgaben, markiert Kandidaten für Commit/Deploy.

### 2) Junior Agent (Generator)
- Rolle: Task‑Executor, erzeugt Code, Raws, Vorschläge, Drafts.
- Rechte: Schreiben in isoliertes Arbeitsverzeichnis, Erstellen von PR‑Drafts (nicht pushen).
- Verhalten: Arbeitet in Iterationszyklen; kann Autoyes‑Simulationen durchführen, aber alle Aktionen sind audit‑tagged.

### 3) Git Agent (Controlled Push Proxy)
- Rolle: Verantwortlich für alle repo‑operationen (commit, branch, push), ausgeführt **nur** auf Host mit Schlüsselmaterial.
- Rechte: Zugriff auf Git‑Credentials (nur auf Host), Schreibrechte nur zu definierten Subpaths.
- Verhalten: Prüft Signaturen der Changes, führt Pre‑Push Checks, optional: require Senior Approval for public pushes.

### 4) AutoUpdater / AutoBuilder
- Rolle: Automatische Codeformattierung, Testausführung, Build‑Pipeline Trigger.
- Rechte: read/write in Build‑Area; keine direkten Push‑Rechte.
- Verhalten: Nur CI‑style operationen; Ergebnisse an Dashboard / Senior.

### 5) Sentinel / Supervisor Agent
- Rolle: Überwacht Betriebsmetriken, Log‑Anomalien, Netzwerkverkehr, Agentenverhalten.
- Rechte: Read‑Only auf Logs, kann Agenten pausieren/quarantäne setzen (via Orchestrator API).
- Verhalten: Laufende Heuristik + regelbasierte Policies; Alarmierung an menschlichen Admin.

### 6) Orchestrator / Coordinator
- Rolle: Start/Stop/Scale von Agenten, Ressourcensteuerung, Priorisierung.
- Rechte: Management APIs, keine direkte Code‑Änderung.
- Verhalten: Implementiert Graceful Degradation, Scheduling, Backpressure.

### 7) Dashboard (Perception Layer)
- Rolle: Sicht auf Systemzustände, Taskqueues, Drafts, Sicherheitswarnungen.
- Rechte: Anzeige + Confirm UI für kritische Aktionen.
- Verhalten: Markiert simulierte vs. reale Aktionen deutlich; Confirmation required flags.

### 8) Persistence & Audit Store
- Rolle: Unveränderliche Speicherung von Aktionen, Agent‑Decisions, signed events.
- Technikidee: Append‑only Log, Hashchain oder lightweight ledger für Nachvollziehbarkeit.

### 9) Network & Security Layer
- Rolle: TLS/MTLS für Agent-Kanäle, JWT/PKI für Agent‑Identities, per‑agent ACLs.
- Verhalten: Agent onboarding mit key provisioning, regelmäßige key‑rotation.

---

## Datenfluss (Sequenzbeispiel)
1. User Input → Dashboard (annotated) → enqueued as Task.
2. Orchestrator assigns Task → Junior Agent pulls Task.
3. Junior generates Drafts, tags actions, writes to Working Dir.
4. Sentinel analyzes Junior behaviour in real‑time.
5. Senior fetches Draft, validates, annotates; if OK → mark for Commit.
6. Git Agent (on Host) pulls signed commit request → runs pre‑push checks → requires either auto‑approval policy or explicit Senior confirm.
7. Push happens; Persistence stores signed event.

---

## Permissions Matrix (Kurz)
- Junior: write -> /work/junior/* ; no git push; no network egress out of allowed domains
- Senior: read -> /work/* ; propose commits; annotate; no direct push
- Git Agent: push rights on Host only; signed commits; limited to repo/subpaths
- Sentinel: read logs; pause Agents via Orchestrator
- Orchestrator: manage processes, resource quotas

---

## Quarantäne & Rollback
- Jede Änderung führt zu einem temporären branch in lokalem repo, signiert und timestamped.
- Push in _public_ branch erfordert explicit quorum (Senior approve or offline signed key).
- Rollback: Git Agent kann automated revert on failure; persistent audit zeigt chain of causality.

---

## Monitoring, Alerts & KPI
- Agent‑Health (heartbeat) — Alert wenn heartbeat > threshold
- Task Throughput / Success Rate
- Anomalies: sudden spikes in added files, large zip writes
- Security alerts: signature mismatches, unauthorized push attempts

---

## Adaptive Policies & Rate Limits
- Autoyes cycles limited per time window (configurable), e.g. 7 cycles normal, > threshold require Senior override.
- Auto‑push: only allowed if tests pass & Sentinel reports no anomalies.
- Resource Cap: per‑agent CPU/IO quota.

---

## Dev / Deploy Workflow Vorschlag
1. Local host (owner) holds master Git key & Push privileges.
2. Agents run in containerized envs (Docker / Podman) with constrained volumes.
3. CI Pipeline (AutoUpdater) runs tests; artifacts are stored in artifact repo.
4. Senior manual checkpoints for any public release.

---

## Beispiel-Use‑Cases
- **Safe Auto‑Commit:** Junior produziert patch -> Senior validates -> Git Agent on host signs & pushes to private branch -> CI runs -> Dashboard alerts human for public release.
- **Emergency Pause:** Sentinel detects anomalous file creation -> Orchestrator pauses Junior -> Human inspects -> action: quarantine/rollback.

---

## Vorschlag Tech‑Stack (Beispiele)
- Containerization: Docker, Podman
- Orchestration: Nomad / systemd / lightweight k8s (k3s) für lokale Setups
- Messaging: NATS / RabbitMQ (mTLS) oder ZeroMQ with mTLS
- Identity: PKI, Key Vault (HashiCorp Vault or OS keyring) for host keys
- Logs & Audit: Elastic Stack / Loki + Append‑only hashchain overlay
- CI: GitHub Actions (local runner) or GitLab CI with host runner

---

## Priorisierte Checkliste (MVP → Hardened)
1. MVP: Junior + Senior + Local Git Agent + Dashboard (manual confirm for pushes)
2. + Sentinel + Orchestrator (basic pause/kill) + Persistence logging
3. + PKI onboarding + signed messages + key rotation
4. + Quarantine / rollback automation + anomaly detection heuristics
5. + Rate limiting, resource quotas, CI gating for public pushes

---

## Open Questions / Entscheidungen
- Wie streng soll "public" definiert sein (nur private repo vs. public GitHub org)?
- Welche Rollen erhalten Offline Approval Keys? (number of trusted humans?)
- Wie viele autoyes cycles sind praktikabel bevor ein mensch einschreiten muss?
- Wieviel der Dashboard Anzeigen dürfen simuliert sein? (Transparenz vs. Noise)

---

## Nächste Schritte
1. Review dieses Dokuments, Kommentar‑Round mit Stakeholdern.
2. Konkrete Architektur‑Diagramme (UML / C4) erstellen.
3. Mini‑MVP implementieren: containerized Junior + Senior + Local Git Agent + Dashboard.
4. Sentinel‑Ruleset (erste heuristics) definieren.

---

*Ende — Draft v0.1*

