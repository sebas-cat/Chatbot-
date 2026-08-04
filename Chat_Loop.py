
import torch
from data.Dataset import label2id, id2label 
import warnings
from src.model import load_model
warnings.filterwarnings("ignore")  
from src.ner import analyze, resolve_date, extract_task
from src.calendar_api import create_event, authenticate_google_calendar
from src.database import init_database, save_event
from src.llm import generate_response


cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")

device = torch.device("cuda" if cuda_available else "cpu")
print(f"Using: {device}")

model_name = "saved_model"  

model, tokenizer = load_model(device, model_name, label2id, id2label)
init_database()
print("PlaseholderChatBotname, Say Bye to quit.\n", flush=True)
service = authenticate_google_calendar()
while True:
    user_input = input("Me: ")
    if user_input == "":
        print("I need a imput to proceed ")
        continue
    if user_input.lower() == "bye":
        print("Bye! Be back soon.")
        break

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
        if "/" not in date:
            date = resolve_date(date)

        if result["time"]:
            is_pm = "pm" in result["time"][0]
            raw_time = result["time"][0].replace("am", "").replace("pm", "").strip()
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
    generated_response = generate_response(user_input, intent, context)
    print(f"Bot: {generated_response}")
            
        