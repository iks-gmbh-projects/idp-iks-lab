# ADR 0002: Kubernetes aus dem MVP ausklammern

## Status

Angenommen

## Kontext

Der erste Nutzen soll ueber Service-Auffindbarkeit, Ownership, Dokumentation und IKS-Metadaten entstehen. Kubernetes wuerde den MVP technisch groesser machen und den Fokus in Richtung Runtime-Integration verschieben.

## Entscheidung

Kubernetes, Deployment-Status und Runtime-Health werden im MVP nicht umgesetzt. Die Struktur bleibt so vorbereitet, dass Kubernetes spaeter als zusaetzliche Datenquelle integriert werden kann.

## Konsequenzen

- Der MVP bleibt leichter und schneller demonstrierbar.
- Der Katalog kann unabhaengig von einer Cluster-Strategie wachsen.
- Runtime- und Health-Daten muessen spaeter gezielt nachgezogen werden.
