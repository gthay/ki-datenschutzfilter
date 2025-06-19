from fastapi import FastAPI, Request
from pydantic import BaseModel
import spacy
import re
import pandas as pd

# Lade das deutsche Sprachmodell
nlp = spacy.load("de_core_news_md")

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/anonymize")
async def anonymize(input: TextInput):
    text = input.text
    doc = nlp(text)
    replacements = []

    # spaCy-NER
    for ent in doc.ents:
        original = ent.text
        replacement = None

        if ent.label_ == "PER":
            parts = original.split()
            if len(parts) == 1:
                replacement = "[VORNAME]"
            elif len(parts) >= 2:
                replacement = "[VORNAME] [NACHNAME]"
            else:
                replacement = "[NAME]"
        elif ent.label_ in ["LOC", "GPE"]:
            if "straße" in original.lower() or "str." in original.lower() or "allee" in original.lower():
                replacement = "[ADDRESS]"
            else:
                replacement = "[CITY]"
        else:
            replacement = f"[{ent.label_}]"

        if replacement:
            replacements.append((original, replacement))

    # Regex-Muster
    regex_patterns = [
        (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL]'),
        (r'(?:(?:\+|00)49|0)[\s\-]?(?:\(?\d{2,5}\)?[\s\-]?)?\d{3,}[\s\-]?\d{3,}', '[PHONE]'),
        (r'\b([A-ZÄÖÜ][a-zäöüß]+(?:straße|strasse|Str\.|weg|Allee|Gasse|Platz))\s?\d{1,4}\b', '[ADDRESS]'),
        (r'\b\d{5}\b', '[ZIP]'),
        (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]'),
        (r'\b(Bestellnummer|Order ID|Bestellung)[\s#:]*[A-Z0-9-]{5,}\b', '[ORDER_ID]'),
        (r'\b(Benutzername|Username|User|Login)[\s:]*[a-zA-Z0-9_.-]{3,}\b', '[USERNAME]'),
        (r'\bKunden[- ]?Nr\.?:?\s?\d{4,}\b', '[CUSTOMER_ID]'),
        (r'\b\d{8,20}\b', '[ACCOUNT_NR]')
    ]

    for pattern, label in regex_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            replacements.append((match, label))

    # Deduplizieren und sortieren (längere zuerst)
    seen = set()
    unique_replacements = []
    for orig, repl in sorted(replacements, key=lambda x: -len(x[0])):
        if orig not in seen:
            unique_replacements.append((orig, repl))
            seen.add(orig)

    # Text ersetzen
    for orig, repl in unique_replacements:
        text = text.replace(orig, repl)

    return {
        "anonymized": text,
        "replacements": [{"original": o, "replaced_with": r} for o, r in unique_replacements]
    }
