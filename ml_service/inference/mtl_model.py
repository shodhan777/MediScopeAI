import torch
import torch.nn as nn

class MultiTaskNet(nn.Module):
    def __init__(self, input_dim):
        super(MultiTaskNet, self).__init__()
        
        # Shared Representation Layers
        self.shared_fc1 = nn.Linear(input_dim, 64)
        self.shared_bn1 = nn.BatchNorm1d(64)
        self.shared_relu1 = nn.ReLU()
        self.shared_dropout1 = nn.Dropout(0.3)
        
        self.shared_fc2 = nn.Linear(64, 32)
        self.shared_bn2 = nn.BatchNorm1d(32)
        self.shared_relu2 = nn.ReLU()
        self.shared_dropout2 = nn.Dropout(0.3)
        
        # Heart Disease Head
        self.heart_fc = nn.Linear(32, 16)
        self.heart_relu = nn.ReLU()
        self.heart_out = nn.Linear(16, 1)
        
        # Diabetes Head
        self.diabetes_fc = nn.Linear(32, 16)
        self.diabetes_relu = nn.ReLU()
        self.diabetes_out = nn.Linear(16, 1)
        
        # Stroke Head
        self.stroke_fc = nn.Linear(32, 16)
        self.stroke_relu = nn.ReLU()
        self.stroke_out = nn.Linear(16, 1)
        
    def forward(self, x):
        # Shared processing
        x = self.shared_fc1(x)
        x = self.shared_bn1(x)
        x = self.shared_relu1(x)
        x = self.shared_dropout1(x)
        
        x = self.shared_fc2(x)
        x = self.shared_bn2(x)
        x = self.shared_relu2(x)
        shared_rep = self.shared_dropout2(x)
        
        # Heart prediction
        h = self.heart_fc(shared_rep)
        h = self.heart_relu(h)
        out_heart = torch.sigmoid(self.heart_out(h))
        
        # Diabetes prediction
        d = self.diabetes_fc(shared_rep)
        d = self.diabetes_relu(d)
        out_diabetes = torch.sigmoid(self.diabetes_out(d))
        
        # Stroke prediction
        s = self.stroke_fc(shared_rep)
        s = self.stroke_relu(s)
        out_stroke = torch.sigmoid(self.stroke_out(s))
        
        return out_heart, out_diabetes, out_stroke

def get_mtl_model(input_dim):
    return MultiTaskNet(input_dim)
