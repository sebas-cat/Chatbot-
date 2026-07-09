from data.Dataset import dataset, label2id, id2label 
import torch
from transformers import AutoTokenizer
from src.model import load_model
from torch.optim import AdamW


labels = []
texts = []
for item in dataset:

    texts.append(item[ "text" ])

    labels.append(label2id[item["label"]])

cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")


device = torch.device("cuda" if cuda_available else "cpu")
print(f"Using: {device}")

model_name = "distilbert-base-multilingual-cased"  

model, tokenizer = load_model(device, model_name, label2id, id2label)

encoding = tokenizer(
        texts,
        truncation=True,
        return_tensors="pt",
        padding=True          
    ).to(device)

labels_tensor = torch.tensor(labels).to(device)

optimizer = AdamW(model.parameters(), lr=2e-5)
epochs = 10

for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    output = model(**encoding, labels=labels_tensor)
    loss = output.loss
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch + 1}, Loss; {loss.item()}")