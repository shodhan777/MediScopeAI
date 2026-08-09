import torch
import shap
import numpy as np

from preprocessing.mtl_adapter import MTL_FEATURES
from inference.mtl_model import get_mtl_model

class MTLExplainer:
    def __init__(self, model_path='models/multitask/mtl_model.pth', background_data=None):
        self.model = get_mtl_model(len(MTL_FEATURES))
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        
        # If no background provided, create a dummy background of zeros
        if background_data is None:
            background_data = torch.zeros((100, len(MTL_FEATURES)))
            
        # SHAP expects a model that outputs a single tensor, but our MTL outputs a tuple of 3.
        # We wrap the model for each disease
        class HeartWrapper(torch.nn.Module):
            def __init__(self, m): super().__init__(); self.m = m
            def forward(self, x): return self.m(x)[0]
            
        class DiabetesWrapper(torch.nn.Module):
            def __init__(self, m): super().__init__(); self.m = m
            def forward(self, x): return self.m(x)[1]
            
        class StrokeWrapper(torch.nn.Module):
            def __init__(self, m): super().__init__(); self.m = m
            def forward(self, x): return self.m(x)[2]
            
        self.explainer_h = shap.DeepExplainer(HeartWrapper(self.model), background_data)
        self.explainer_d = shap.DeepExplainer(DiabetesWrapper(self.model), background_data)
        self.explainer_s = shap.DeepExplainer(StrokeWrapper(self.model), background_data)

    def explain(self, x_tensor, disease='heart'):
        if disease == 'heart':
            shap_values = self.explainer_h.shap_values(x_tensor, check_additivity=False)
        elif disease == 'diabetes':
            shap_values = self.explainer_d.shap_values(x_tensor, check_additivity=False)
        else:
            shap_values = self.explainer_s.shap_values(x_tensor, check_additivity=False)
            
        # DeepExplainer returns a list if multiple outputs, or array
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
            
        shap_vals = shap_values[0] # batch size 1
        
        # Map to features
        factors = []
        import numpy as np
        for i, val in enumerate(shap_vals):
            v = float(np.sum(val))
            if abs(v) > 1e-4:  # filter noise
                factors.append({
                    "feature": MTL_FEATURES[i],
                    "impact": abs(v),
                    "direction": "increases_risk" if v > 0 else "decreases_risk"
                })
                
        # Sort by impact
        factors = sorted(factors, key=lambda x: x['impact'], reverse=True)
        return factors[:5] # Top 5
