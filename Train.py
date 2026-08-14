from data.Dataset import dataset, label2id, id2label 
import torch
from transformers import AutoTokenizer
from src.model import load_model
from torch.optim import AdamW
from torch.utils.data import DataLoader, TensorDataset


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

dataset_tensor = TensorDataset(
    encoding["input_ids"],
    encoding["attention_mask"],
    labels_tensor
)
loader = DataLoader(dataset_tensor, batch_size = 4, shuffle = True)

optimizer = AdamW(model.parameters(), lr=2e-5)
epochs = 20

for epoch in range(epochs):
    model.train()
    total_loss = 0
    for input_ids, attention_mask, batch_labels in loader:
        optimizer.zero_grad()
        output = model(input_ids=input_ids, attention_mask=attention_mask, labels= batch_labels)
        loss = output.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(loader)
    print(f"Epoch {epoch + 1}, Loss; {avg_loss}")

model.save_pretrained("saved_model")
tokenizer.save_pretrained("saved_model")