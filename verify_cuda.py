import torch

if torch.cuda.is_available():
    print("CUDA is available. PyTorch is using GPU.")
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. PyTorch is using CPU.")
