# step3_chat_loop.py

import torch
import warnings
from src.model import load_model
warnings.filterwarnings("ignore")  

cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")


device = torch.device("cuda" if cuda_available else "cpu")
print(f"Using: {device}")

model_name = "distilgpt2"  

model, tokenizer = load_model(device, model_name)

print("PlaseholderChatBotname, Say Bye to quit.\n", flush=True)

while True:
    user_input = input("Me: ")
    if user_input == "":
        print("I need a imput to proceed ")
        continue
    if user_input.lower() == "Bye":
        print("Bye! Be back soon.")
        break

    inputs = tokenizer(
        user_input,
        return_tensors="pt",
        padding=True          
    ).to(device)

    with torch.no_grad():
        output_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"], 
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )

    input_length = inputs["input_ids"].shape[1]
    response = tokenizer.decode(
        output_ids[0][input_length:],
        skip_special_tokens=True
    )

    print(f"Bot: {response}\n")