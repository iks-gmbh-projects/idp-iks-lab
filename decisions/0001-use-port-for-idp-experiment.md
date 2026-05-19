# ADR 0001: Port fuer das IDP-Experiment verwenden

## Status

Angenommen

## Kontext

Das Experiment soll mit einem Service-Katalog starten, spaeter aber Workflows, Automationen und Agenten aufnehmen koennen. Backstage OSS ist sehr flexibel, benoetigt aber mehr Eigenbetrieb und Entwicklungsaufwand.

## Entscheidung

Port wird als Zielplattform fuer den MVP verwendet. GitHub dient als versionierte Source of Truth fuer Konfiguration, Beispiel-Entities und Dokumentation.

## Konsequenzen

- Schnellerer Start fuer Katalog, Scorecards und Actions.
- Flexibles Datenmodell fuer IKS-Metadaten.
- Weniger Eigenbetrieb als bei einem selbst betriebenen Backstage.
- Abhaengigkeit von Port als kommerziellem Portalprodukt.
