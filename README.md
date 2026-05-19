# IDP IKS Lab

Dieses Repository ist der Startpunkt fuer ein experimentelles Internal Developer Platform MVP fuer die IKS. Der Fokus liegt auf einem Port-basierten Service-Katalog, der Ownership, Dokumentation, IKS-Metadaten, Scorecards und einfache Workflows sichtbar macht.

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

- `docs/`: Zielbild, Demo-Story, Betriebsmodell und IKS-Metadatenmodell.
- `port/blueprints/`: Port-Datenmodell fuer Katalogobjekte.
- `port/entities/`: Beispielhafte Katalogdaten.
- `port/scorecards/`: Erste Qualitaets- und IKS-Pruefregeln.
- `port/actions/`: Vorbereitete Self-Service-Workflows.
- `examples/services/`: Beispiel-Services mit Doku und Katalogdaten.
- `decisions/`: Architekturentscheidungen.
- `agents/`: Agentenleitfaden, wiederverwendbare Prompts, Checklisten und Codex-Skills.

## Naechste Schritte

1. Repository auf GitHub veroeffentlichen.
2. Port Workspace anlegen.
3. GitHub als Datenquelle in Port verbinden.
4. Blueprints und Entities importieren oder ueber Port Ocean synchronisieren.
5. Scorecards und Actions gegen die Demo-Services testen.
