import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
def load_model(device, model_name):
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype = torch.float32
)
    model = model.to(device)
    model.eval()
    return model, tokenizer

    
    
    
