# IKS-Metadatenmodell

Dieses Dokument beschreibt die ersten Pflichtfelder fuer Services im Katalog. Die Felder sind bewusst klein gehalten, damit Teams schnell onboarden koennen.

## Pflichtfelder fuer Services

| Feld | Zweck | Beispiel |
|---|---|---|
| `technicalOwner` | Technische Verantwortung | `platform-team` |
| `businessOwner` | Fachliche Verantwortung | `customer-success` |
| `lifecycle` | Reifegrad des Services | `experimental`, `production`, `deprecated` |
| `criticality` | Auswirkung bei Ausfall | `low`, `medium`, `high`, `critical` |
| `protectionNeed` | Schutzbedarf | `normal`, `high`, `very-high` |
| `dataClass` | Datenklasse | `public`, `internal`, `confidential`, `personal-data` |
| `repository` | Code-Quelle | GitHub Repository URL |
| `documentation` | Technische Doku | Docs URL |
| `runbook` | Betriebsanleitung | Runbook URL |

## Optionale Felder

- `system`: Zugehoeriges fachliches oder technisches System.
- `tier`: Service-Tier fuer Betrieb und Support.
- `complianceScope`: Relevante Kontrollrahmen, z. B. `iks`, `gdpr`, `nis2`.
- `lastReviewDate`: Datum der letzten fachlichen oder IKS-Pruefung.

## MVP-Regel

Ein Service gilt im MVP als katalogfaehig, wenn mindestens Owner, Lifecycle, Repository, Dokumentation, Kritikalitaet, Schutzbedarf und Datenklasse gepflegt sind.
