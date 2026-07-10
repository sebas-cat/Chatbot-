
import torch
from data.Dataset import label2id, id2label 
import warnings
from src.model import load_model
warnings.filterwarnings("ignore")  

cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")

device = torch.device("cuda" if cuda_available else "cpu")
print(f"Using: {device}")

model_name = "saved_model"  

model, tokenizer = load_model(device, model_name, label2id, id2label)

print("PlaseholderChatBotname, Say Bye to quit.\n", flush=True)

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
        print(intent)