import torch  

cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")


device = torch.device("cuda" if cuda_available else "cpu")
print(f"Using device: {device}")


if device.type == "cuda":
    gpu_name = torch.cuda.get_device_name(0)  
    vram_total = torch.cuda.get_device_properties(0).total_memory / 1e9  
    print(f"GPU: {gpu_name}")
    print(f"VRAM: {vram_total:.1f} GB")