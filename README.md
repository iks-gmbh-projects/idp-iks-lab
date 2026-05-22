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
- Dokumentierter lokaler Backstage-MVP-Pfad unter `backstage/runtime/`, der eine extern generierte Runtime auf diesen Repository-Katalog zeigt.
- Wiki-Dokumentation als Submodul unter `wiki/`.
- Agenten-Artefakte unter `agents/` mit Prompts, Checklisten und repo-versionierten Skills.

Noch offen fuer den MVP-Betrieb:

- Lokalen Backstage-MVP ueber die dokumentierte externe Runtime unter `backstage/runtime/` starten und validieren.
- Spaeter entscheiden, ob eine lauffaehige Backstage-App dauerhaft in dieses Repository aufgenommen wird oder extern bleibt.
- Catalog-Views und Demo-Navigation gemaess `backstage/catalog/demo-views.md` pruefen.
- Scorecard-Ansatz finalisieren: Tech Insights, Scorecard-Plugin oder GitHub-basierter Report.
- Backstage-Templates fuer GitHub-Issue-Erzeugung mit echten Zugangsdaten testen.
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
2. Catalog-Views fuer alle Services, IKS-relevante Services und kritische Services werden gemaess `backstage/catalog/demo-views.md` geprueft.
3. Ein Service wird geoeffnet und zeigt Owner, Lifecycle, Doku und IKS-Metadaten.
4. Scorecards oder Backstage-Checks markieren vollstaendige und unvollstaendige Metadaten.
5. Ein Software Template oder GitHub Issue Form erzeugt eine Review- oder Katalogpflege-Aufgabe in GitHub.
6. Die vorbereiteten Agenten- und Workflow-Artefakte zeigen den Ausbaupfad.

## Struktur

- `.github/workflows/`: aktive GitHub-Actions-Workflows.
- `.github/dependabot.yml`: Dependabot-Konfiguration fuer Wartung von npm- und GitHub-Actions-Abhaengigkeiten.
- `github/workflows/`: Workflow-Vorlagen und Referenzkopien.
- `github/issue-templates/`: GitHub-Issue-Templates fuer vorbereitete Workflows.
- `wiki/docs/`: Zielbild, Demo-Story, Betriebsmodell und IKS-Metadatenmodell als GitHub-Wiki-Submodul.
- `wiki/decisions/`: Architekturentscheidungen als Teil des GitHub-Wiki-Submoduls.
- `backstage/`: Backstage-Zielstruktur fuer Catalog-Locations, Beispielkonfiguration, lokale Runtime-Hinweise, Templates, TechDocs und Scorecard-Mapping.
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

1. Lokale Backstage-Runtime gemaess `backstage/runtime/README.md` erzeugen oder vorhandene Instanz verwenden.
2. `backstage/catalog/locations.yaml` als Catalog-Location anbinden.
3. Demo-Entities und Service-nahe `catalog-info.yaml` Dateien importieren.
4. TechDocs fuer die Beispielservices pruefen.
5. Scorecard-/Tech-Insights-Ansatz fuer Katalogqualitaet und IKS-Basisdaten entscheiden.
6. Templates oder GitHub Issue Forms fuer Review- und Katalogpflege-Workflows testen.
7. Catalog-Views gemaess `backstage/catalog/demo-views.md` und Demo-Ablauf aus `wiki/docs/demo-story.md` end-to-end pruefen.
