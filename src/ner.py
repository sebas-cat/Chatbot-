import spacy
import re

nlp = spacy.load("es_core_news_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = ent.text 
    return entities 


def extract_dates(text):
    pattern = (r"lunes|martes|miércoles|jueves|viernes|sábado|domingo")
    pattern2 = (r"\d{1,2}\/\d{1,2}\/\d{2,4}")
    matches = re.findall(pattern, text)
    matches2 = re.findall(pattern2, text)
    return matches + matches2

def analyze(text):
    entities = extract_entities(text)
    dates = extract_dates(text)
    results = {"entities": entities, "dates": dates}
    return results