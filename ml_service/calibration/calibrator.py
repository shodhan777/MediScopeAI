import torch
import torch.nn as nn
import numpy as np

class TemperatureScaler(nn.Module):
    """
    Applies temperature scaling to model logits (pre-sigmoid) to calibrate probabilities.
    Since our model outputs sigmoids, we can inverse sigmoid to get logits, scale, and re-apply sigmoid.
    """
    def __init__(self, temperature=1.5):
        super().__init__()
        self.temperature = nn.Parameter(torch.ones(1) * temperature)
        
    def forward(self, probs):
        # Inverse sigmoid (logit)
        eps = 1e-7
        probs = torch.clamp(probs, eps, 1.0 - eps)
        logits = torch.log(probs / (1.0 - probs))
        
        # Scale
        scaled_logits = logits / self.temperature
        
        # Re-apply sigmoid
        calibrated_probs = torch.sigmoid(scaled_logits)
        return calibrated_probs

def calibrate_prediction(prob, temperature=1.5):
    scaler = TemperatureScaler(temperature=temperature)
    prob_tensor = torch.tensor([prob], dtype=torch.float32)
    calibrated = scaler(prob_tensor)
    return calibrated.item()
