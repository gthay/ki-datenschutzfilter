# KI-Datenschutzfilter
KI-Datenschutzfilter ist ein Datenschutz-Tool, das Texte automatisch von personenbezogenen Daten befreit, um eine DSGVO-konforme Nutzung von KI-Modellen zu ermöglichen.

## ✅ Welche Daten werden entfernt?
Folgende personenbezogene Daten werden automatisch erkannt und ersetzt:

- 🧑 Namen (Vor- und Nachname)
- 🏠 Adressen (Straßenname, Stadt, PLZ)
- 📧 E-Mail-Adressen
- 📞 Telefonnummern
- 🌐 IP-Adressen

## Wie funktioniert die Ersetzung
Das Entfernen von Namen und Adressen funktioniert über das Skript spacy.io welches darauf trainiert ist, Text zu verstehen. Dabei handelt es sich um keine KI und kein LLM, sondern um ein Skript. Andere Daten, wie E-Mail-Adressen, Telefonnummern und IP-Adressen, werden mithilfe von RegEx entfernt.

## ⚙️ Wie funktioniert die Anonymisierung?

| Datentyp         | Erkennungsmethode                    | Ersetzung                |
|------------------|--------------------------------------|--------------------------|
| **Name**         | `spaCy` NER (Label: `PER`)           | `[VORNAME] [NACHNAME]`   |
| **Adresse**      | `spaCy` NER (`LOC`, `GPE`) + RegEx   | `[ADRESSE]`              |
| **E-Mail-Adresse** | RegEx                              | `[EMAIL]`                |
| **Telefonnummer**  | RegEx                              | `[TELEFON]`              |
| **IP-Adresse**     | RegEx                              | `[IP]`                   |
| **Benutzername**   | (optional/noch nicht implementiert) |                          |
| **Kundennummern**  | (optional/noch nicht implementiert) |                          |

## 🧠 Warum spaCy und nicht ein KI-Modell?
Das Tool verwendet kein LLM, sondern die bewährte NLP-Bibliothek spaCy. Dadurch ist es:

- schnell & ressourcenschonend
- lokal ausführbar
- rechtlich sicherer (keine Datenübertragung an externe APIs)

## 📦 Einsatzmöglichkeiten
- DSGVO-konforme Vorverarbeitung von Textdaten
- Vorbereitung sensibler Inhalte für KI-Modelle (z. B. GPT, Mistral, LLaMA)
- Automatisierter Datenschutz in Unternehmen

## Installation
Kopiere den Link zu diesem Repository, öffne Coolify auf deinem VPS. Füge einen Service hinzu und wähle ganz oben "Public Repository" in der Git-Sektion. Füge den Link zu dieser Seite ein und drücke auf Deploy. Dann kannst du mithilfe von n8n.io z.B. und einem HTTP Node, dieses Skript abfragen.

## ⚠️ Haftungsausschluss / Disclaimer

> **Dieses Tool bietet keine Garantie auf vollständige Anonymisierung.**  
> Obwohl KI-Datenschutzfilter viele gängige personenbezogene Daten zuverlässig erkennt und entfernt, kann **keine 100%ige Erkennung aller sensiblen Informationen** gewährleistet werden.  
> Die Nutzung erfolgt auf eigene Verantwortung. Vor dem Einsatz in produktiven oder rechtlich sensiblen Umgebungen wird eine **manuelle Prüfung der anonymisierten Daten empfohlen.**  
>  
> Dieses Projekt stellt **keine Rechtsberatung** dar. Bei Unsicherheiten bezüglich DSGVO-Konformität sollte juristischer Rat eingeholt werden.
