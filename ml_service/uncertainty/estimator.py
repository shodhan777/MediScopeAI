import torch
import numpy as np

def get_mc_dropout_uncertainty(model, x_tensor, n_iterations=20):
    """
    Enable dropout layers during evaluation to estimate uncertainty.
    Returns the mean prediction and variance/std.
    """
    # Keep batchnorm in eval mode to avoid batch size 1 crash, but enable dropout
    model.eval()
    def enable_dropout(m):
        if type(m) == torch.nn.Dropout:
            m.train()
    model.apply(enable_dropout)
    
    h_preds = []
    d_preds = []
    s_preds = []
    
    with torch.no_grad():
        for _ in range(n_iterations):
            h, d, s = model(x_tensor)
            h_preds.append(h.item())
            d_preds.append(d.item())
            s_preds.append(s.item())
            
    model.eval() # Revert back to eval mode
    
    return {
        'heart': {'mean': np.mean(h_preds), 'std': np.std(h_preds)},
        'diabetes': {'mean': np.mean(d_preds), 'std': np.std(d_preds)},
        'stroke': {'mean': np.mean(s_preds), 'std': np.std(s_preds)}
    }

def calculate_confidence(std_dev):
    """
    Thresholds for uncertainty. High std dev means low confidence.
    """
    if std_dev < 0.05:
        return "HIGH"
    elif std_dev < 0.15:
        return "MEDIUM"
    else:
        return "LOW"
