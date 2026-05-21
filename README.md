# IDP IKS Lab

Dieses Repository ist der Startpunkt fuer ein experimentelles Internal Developer Platform MVP fuer die IKS. Der Fokus verschiebt sich auf einen Backstage-basierten, selbstgehosteten Service-Katalog, der Ownership, Dokumentation, IKS-Metadaten, Scorecards und einfache Workflows sichtbar macht.

GitHub ist die versionierte Source of Truth fuer Backstage-Katalogdaten, Konfiguration, Demo-Entities, Entscheidungen, Dokumentation und Agenten-Artefakte.

## Projektstatus

Vorhanden im Repository:

- Erste Port-Artefakte fuer Blueprints, Demo-Entities, Scorecards und Actions als Migrationsreferenz aus dem initialen Experiment.
- Backstage-Zielstruktur unter `backstage/` fuer Catalog-Locations, Beispielkonfiguration, Templates und Scorecard-Mapping.
- Backstage-native Demo-Entities fuer Teams, Systeme und Services.
- Zwei Demo-Services: `customer-portal` als weitgehend vollstaendiges Beispiel und `reporting-api` mit bewusst fehlendem Runbook-Link.
- GitHub-Issue-Forms fuer Katalogpflege und IKS-Reviews.
- Aktive GitHub-Actions-Validierung fuer YAML-Dateien in `backstage`, `port`, `examples`, `agents` und `.github/ISSUE_TEMPLATE`.
- Wiki-Dokumentation als Submodul unter `wiki/`.
- Agenten-Artefakte unter `agents/` mit Prompts, Checklisten und repo-versionierten Skills.

Noch offen fuer den MVP-Betrieb:

- Entscheiden, ob dieses Repository nur Backstage-Katalog-/Konfigurationsquelle bleibt oder spaeter auch eine lauffaehige Backstage-App enthaelt.
- Backstage-Instanz lokal oder selbstgehostet bereitstellen.
- Catalog-Locations aus `backstage/catalog/locations.yaml` in Backstage einbinden.
- Demo-Services ueber `catalog-info.yaml` pruefen.
- Scorecard-Ansatz finalisieren: Tech Insights, Scorecard-Plugin oder GitHub-basierter Report.
- Backstage-Templates fuer GitHub-Issue-Erzeugung mit echten Zugangsdaten testen.
- Demo end-to-end trocken laufen lassen.

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
- IKS-relevante Metadaten versioniert in GitHub pflegen.
- Katalogqualitaet und IKS-Basisdaten ueber Scorecards oder gleichwertige Backstage-Checks sichtbar machen.
- Erste risikoarme Workflows vorbereiten, zum Beispiel GitHub Issues fuer fehlende Metadaten oder IKS-Reviews.
- Eine spaetere Erweiterung um Agenten und Kubernetes offenhalten.

## Nicht-Ziele im MVP

- Kein Kubernetes- oder Runtime-Health-Dashboard.
- Keine automatische Infrastruktur-Provisionierung.
- Keine autonom handelnden Agenten.
- Keine vollstaendige Compliance-Automatisierung.

## Demo-Ablauf

1. Backstage zeigt Teams, Systeme und Demo-Services im Software Catalog.
2. Ein Service wird geoeffnet und zeigt Owner, Lifecycle, Doku und IKS-Metadaten.
3. Scorecards oder Backstage-Checks markieren vollstaendige und unvollstaendige Metadaten.
4. Ein Software Template oder GitHub Issue Form erzeugt eine Review- oder Katalogpflege-Aufgabe in GitHub.
5. Die vorbereiteten Agenten- und Workflow-Artefakte zeigen den Ausbaupfad.

## Struktur

- `.github/workflows/`: aktive GitHub-Actions-Workflows.
- `.github/dependabot.yml`: Dependabot-Konfiguration fuer Wartung von npm- und GitHub-Actions-Abhaengigkeiten.
- `github/workflows/`: Workflow-Vorlagen und Referenzkopien.
- `github/issue-templates/`: GitHub-Issue-Templates fuer vorbereitete Workflows.
- `wiki/docs/`: Zielbild, Demo-Story, Betriebsmodell und IKS-Metadatenmodell als GitHub-Wiki-Submodul.
- `wiki/decisions/`: Architekturentscheidungen als Teil des GitHub-Wiki-Submoduls.
- `backstage/`: Backstage-Zielstruktur fuer Catalog-Locations, Beispielkonfiguration, Templates, TechDocs und Scorecard-Mapping.
- `examples/services/`: Beispiel-Services mit Doku und Backstage `catalog-info.yaml` Dateien.
- `port/`: Legacy-Migrationsreferenz aus dem initialen Port-Experiment.
- `agents/`: Agentenleitfaden, wiederverwendbare Prompts, Checklisten und Skills.

## Validierung

Die aktive GitHub-Actions-Validierung liegt unter `.github/workflows/validate-idp-config.yml` und prueft YAML-Dateien in `backstage`, `port`, `examples`, `agents` und `.github/ISSUE_TEMPLATE`.

Die Datei `github/workflows/validate-idp-config.yml` bleibt als Vorlage und Referenz fuer die Workflow-Konfiguration erhalten. Beide Dateien sollten bei Aenderungen an der Validierung synchron bleiben.

Die Validierung ist bewusst als Syntax-Check fuer bestehende Backstage-, Legacy-Port-, Beispiel-, Issue-Form- und Agenten-Artefakte ausgelegt. `document-start` und `line-length` sind deaktiviert, damit vorhandene YAML-Dateien nicht wegen Formatstil statt Syntax scheitern.

Lokal kann bei installiertem `yamllint` analog geprueft werden:

```powershell
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
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

1. Backstage-Instanz fuer den MVP bereitstellen oder vorhandene Instanz verwenden.
2. `backstage/catalog/locations.yaml` als Catalog-Location anbinden.
3. Demo-Entities und Service-nahe `catalog-info.yaml` Dateien importieren.
4. TechDocs fuer die Beispielservices pruefen.
5. Scorecard-/Tech-Insights-Ansatz fuer Katalogqualitaet und IKS-Basisdaten entscheiden.
6. Templates oder GitHub Issue Forms fuer Review- und Katalogpflege-Workflows testen.
7. Demo-Ablauf aus `wiki/docs/demo-story.md` end-to-end pruefen.
