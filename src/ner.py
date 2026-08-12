import spacy
import re
import datetime

nlp = spacy.load("es_core_news_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = ent.text 
    return entities 


def extract_dates(text):
    pattern = (r"lunes|martes|miércoles|jueves|viernes|sábado|domingo|mañana|hoy")
    pattern2 = (r"\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}")
    matches = re.findall(pattern, text)
    matches2 = re.findall(pattern2, text)
    return matches + matches2

def analyze(text):
    entities = extract_entities(text)
    dates = extract_dates(text)
    time = extract_time(text)
    results = {"entities": entities, "dates": dates, "time": time}
    return results

days_of_the_week = {"lunes": 0,
            "martes": 1,
            "miércoles": 2,
            "jueves": 3,
            "viernes": 4,
            "sábado": 5,
            "domingo": 6}
def resolve_date(day_name):
    if day_name == "hoy":
        return datetime.date.today().strftime("%Y-%m-%d")
    if day_name == "mañana":
        return (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    target = days_of_the_week[day_name]
    today = datetime.date.today()
    days_ahead = (target - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    result = today + datetime.timedelta(days=days_ahead)
    return result.strftime("%Y-%m-%d")

def extract_time(text):
    Tpattern = r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm)\b|\b\d{1,2}:\d{2}\b"
    Tmatches = re.findall(Tpattern, text)
    return Tmatches

def extract_task(text, dates, time):
    for date in dates:
        text = text.replace(date, "")      
    for t in time:
        text = text.replace(t, "") 
    filler_and_verbs = ["tengo tarea de","Anota que tengo que entregar","Recordarme","Agrega","Crear recordatorio para","necesito entregar","necesito programar","ayúdame a organizar", "a las","el", "la", "los", "las","que", "para", "con", "hola", "antes de medianoche", "mañana", "hoy", "en la tarde", "de", "del", "debe", "debo", "lo primero que debo terminar hoy es", "pon la entrega de", "marca la lectura obligatoria de","a s","s"," a s"]
    for verb in filler_and_verbs:
        text = re.sub(r'\b' + re.escape(verb) + r'\b', '', text, flags=re.IGNORECASE)
    return text.strip()