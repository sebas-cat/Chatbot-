from src.llm import generate_response
from src.database import get_events_date, init_database, save_event
from src.calendar_api import create_event, authenticate_google_calendar
from src.ner import analyze, resolve_date, extract_task
import streamlit as st
import torch
from data.Dataset import label2id, id2label
import warnings
from src.model import load_model
warnings.filterwarnings("ignore")


@st.cache_resource
def initialize():
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    device = torch.device("cuda" if cuda_available else "cpu")
    print(f"Using: {device}")
    model_name = "saved_model"
    model, tokenizer = load_model(device, model_name, label2id, id2label)
    service = authenticate_google_calendar()
    init_database()
    return model, tokenizer, service, device


model, tokenizer, service, device = initialize()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Help me guide you, type what you need...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    inputs = tokenizer(
        user_input,
        return_tensors="pt",
        padding=True
    ).to(device)

    with torch.no_grad():
        output = model(**inputs)
        logits = output.logits
        predicted_id = torch.argmax(logits).item()

    intent = id2label[predicted_id]
    result = analyze(user_input)
    context = {
        "dates": result["dates"],
        "time": result["time"],
        "entities": result["entities"]
    }
    task = extract_task(user_input, result["dates"], result["time"])

    if intent == "work_assignment" and result["dates"]:
        date = result["dates"][0]
        if "/" not in date and "-" not in date:
            date = resolve_date(date)
        elif "/" in date or "-" in date:
            separator = "/" if "/" in date else "-"
            parts = date.split(separator)
            date = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"

        if result["time"]:
            is_pm = "pm" in result["time"][0]
            raw_time = result["time"][0].replace(
                "am", "").replace("pm", "").strip()
            if ":" not in raw_time:
                raw_time = f"{raw_time}:00"
            hour = int(raw_time.split(":")[0])
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            raw_time = f"{hour:02d}:{raw_time.split(':')[1]}"
            start_time = f"{date}T{raw_time}:00"
            end_time = f"{date}T{int(raw_time.split(':')[0])+1:02d}:{raw_time.split(':')[1]}:00"
        else:
            start_time = f"{date}T10:00:00"
            end_time = f"{date}T11:00:00"

        create_event(
            service,
            summary=task,
            description=user_input,
            start_time=start_time,
            end_time=end_time
        )
        save_event(user_input, intent, date, start_time)

    elif intent == "date" and result["dates"]:
        date = result["dates"][0]
        if "/" not in date and "-" not in date:
            date = resolve_date(date)
        elif "/" in date or "-" in date:
            separator = "/" if "/" in date else "-"
            parts = date.split(separator)
            date = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
        events = get_events_date(date)
        context["events"] = events

    elif intent == "conflict" and result["dates"]:
        conflict = result["dates"][0]
        if "/" not in conflict:
            conflict = resolve_date(conflict)
        events = get_events_date(conflict)
        context["conflict_detected"] = len(events) > 1

    generated_response = generate_response(
        user_input, intent, context, st.session_state.messages)

    with st.chat_message("assistant"):
        st.markdown(generated_response)
    st.session_state.messages.append({"role": "assistant", "content": generated_response})

    