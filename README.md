# IDP IKS Lab

Dieses Repository ist der Startpunkt fuer ein experimentelles Internal Developer Platform MVP fuer die IKS. Der Fokus liegt auf einem Port-basierten Service-Katalog, der Ownership, Dokumentation, IKS-Metadaten, Scorecards und einfache Workflows sichtbar macht.

GitHub ist die versionierte Source of Truth fuer Port-Konfiguration, Demo-Entities, Entscheidungen, Dokumentation und Agenten-Artefakte.

## Projektstatus

Vorhanden im Repository:

- Port-Blueprints fuer Teams, Systeme, Repositories, Services, Workflows und Agenten.
- Demo-Entities fuer Teams, Systeme, Repositories, Services und Agenten.
- Zwei Demo-Services: `customer-portal` als weitgehend vollstaendiges Beispiel und `reporting-api` mit bewusst fehlendem Runbook-Link.
- Scorecards fuer Katalogqualitaet und IKS-Basisdaten.
- Vorbereitete Self-Service-Actions fuer Service-Onboarding, IKS-Review und fehlende Metadaten.
- Eine draft-Automation fuer Metadata Drift.
- GitHub-Issue-Templates fuer Katalogpflege und IKS-Reviews.
- Aktive GitHub-Actions-Validierung fuer YAML-Dateien in `port`, `examples` und `agents`.
- Dependabot-Konfiguration fuer npm- und GitHub-Actions-Maintenance.
- Wiki-Dokumentation als Submodul unter `wiki/`.
- Agenten-Artefakte unter `agents/` mit Prompts, Checklisten und repo-versionierten Skills.

Noch offen fuer den MVP-Betrieb:

- Port Workspace anlegen und GitHub anbinden.
- Blueprints und Entities in Port importieren oder synchronisieren.
- Scorecards in Port pruefen und Demo-Views konfigurieren.
- Port-Actions mit der echten GitHub-Issue-Erzeugung verbinden.
- Entscheiden, ob die draft-Automation Teil der Demo bleibt oder als Zukunftspfad gezeigt wird.
- Demo end-to-end trocken laufen lassen.

## Ziele

- Services, Systeme, Teams und Repositories zentral auffindbar machen.
- IKS-relevante Metadaten versioniert pflegen.
- Katalogqualitaet und IKS-Basisdaten ueber Scorecards pruefbar machen.
- Erste risikoarme Workflows vorbereiten, zum Beispiel GitHub Issues fuer fehlende Metadaten oder IKS-Reviews.
- Eine spaetere Erweiterung um Agenten und Kubernetes offenhalten.

## Nicht-Ziele im MVP

- Kein Kubernetes- oder Runtime-Health-Dashboard.
- Keine automatische Infrastruktur-Provisionierung.
- Keine autonom handelnden Agenten.
- Keine vollstaendige Compliance-Automatisierung.

## Demo-Ablauf

1. Port zeigt Teams, Systeme, Repositories und Demo-Services.
2. Ein Service wird geoeffnet und zeigt Owner, Lifecycle, Doku und IKS-Metadaten.
3. Scorecards markieren vollstaendige und unvollstaendige Metadaten.
4. Eine Action erzeugt eine Review- oder Katalogpflege-Aufgabe in GitHub.
5. Die vorbereiteten Agenten- und Workflow-Blueprints zeigen den Ausbaupfad.

## Struktur

- `.github/workflows/`: aktive GitHub-Actions-Workflows.
- `.github/dependabot.yml`: Dependabot-Konfiguration fuer Wartung von npm- und GitHub-Actions-Abhaengigkeiten.
- `github/workflows/`: Workflow-Vorlagen und Referenzkopien.
- `github/issue-templates/`: GitHub-Issue-Templates fuer vorbereitete Workflows.
- `wiki/docs/`: Zielbild, Demo-Story, Betriebsmodell und IKS-Metadatenmodell als GitHub-Wiki-Submodul.
- `wiki/decisions/`: Architekturentscheidungen als Teil des GitHub-Wiki-Submoduls.
- `port/blueprints/`: Port-Datenmodell fuer Katalogobjekte.
- `port/entities/`: Beispielhafte Katalogdaten.
- `port/scorecards/`: Erste Qualitaets- und IKS-Pruefregeln.
- `port/actions/`: Vorbereitete Self-Service-Workflows.
- `port/automations/`: Entwuerfe fuer spaetere Port-Automationen.
- `examples/services/`: Beispiel-Services mit Doku und Katalogdaten.
- `agents/`: Agentenleitfaden, wiederverwendbare Prompts, Checklisten und Skills.

## Validierung

Die aktive GitHub-Actions-Validierung liegt unter `.github/workflows/validate-port-config.yml` und prueft YAML-Dateien in `port`, `examples` und `agents`.

Die Datei `github/workflows/validate-port-config.yml` bleibt als Vorlage und Referenz fuer die Workflow-Konfiguration erhalten. Beide Dateien sollten bei Aenderungen an der Validierung synchron bleiben.

Die Validierung ist bewusst als Syntax-Check fuer bestehende Port-, Beispiel- und Agenten-Artefakte ausgelegt. `document-start` und `line-length` sind deaktiviert, damit vorhandene YAML-Dateien nicht wegen Formatstil statt Syntax scheitern.

Lokal kann bei installiertem `yamllint` analog geprueft werden:

```powershell
yamllint port examples agents
```

## Wiki-Submodul

Die zentrale Projektdokumentation liegt im GitHub-Wiki unter `wiki/`. Beim Klonen sollte das Submodul mitgeladen werden:

```powershell
git clone --recurse-submodules https://github.com/iks-gmbh-projects/idp-iks-lab.git
```

Bei einem bestehenden Clone:

```powershell
git submodule update --init --remote --merge wiki
```

Vor Wiki-Aenderungen:

```powershell
git -C wiki switch master
git -C wiki pull --ff-only
```

Wiki-Aenderungen brauchen zwei Commits: zuerst im `wiki`-Submodul committen und pushen, danach den aktualisierten Submodul-Zeiger im Hauptrepository committen.

## Naechste Schritte

1. Port Workspace anlegen.
2. GitHub als Datenquelle in Port verbinden.
3. Blueprints und Entities importieren oder ueber Port Ocean synchronisieren.
4. Scorecards und Demo-Views in Port konfigurieren.
5. Actions fuer GitHub-Issue-Erzeugung gegen die Demo-Services testen.
6. Metadata-Drift-Automation bewusst als Draft behalten oder fuer die Demo advisory-only ausarbeiten.
7. Demo-Ablauf aus `wiki/docs/demo-story.md` end-to-end pruefen.
