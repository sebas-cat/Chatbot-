import torch
from transformers import AutoTokenizer,  AutoModelForSequenceClassification
def load_model(device, model_name, label2id, id2label ):
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    model =  AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(label2id),
    torch_dtype = torch.float32
)
    model = model.to(device)
    model.eval()
    return model, tokenizer

    
    
    
