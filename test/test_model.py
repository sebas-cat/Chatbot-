import torch
import warnings
from src.model import load_model
from data.Dataset import id2label, label2id


def test_model_loads():
    model_name = "distilbert-base-multilingual-cased"
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    device = torch.device("cuda" if cuda_available else "cpu")
    print(f"Using device: {device}")
    model, tokenizer =  load_model(device, model_name, label2id, id2label)
    
    assert model is not None
    assert tokenizer is not None
