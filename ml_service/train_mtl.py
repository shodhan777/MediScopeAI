import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import json

from preprocessing.mtl_adapter import get_combined_dataset, MTL_FEATURES
from inference.mtl_model import get_mtl_model

def train_model():
    print("Loading data...")
    X, Y = get_combined_dataset()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Save scaler
    joblib.dump(scaler, 'models/multitask/mtl_scaler.pkl')
    
    # Split
    X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)
    
    # Convert to Tensors
    X_train_t = torch.FloatTensor(X_train)
    Y_train_t = torch.FloatTensor(Y_train)
    X_test_t = torch.FloatTensor(X_test)
    Y_test_t = torch.FloatTensor(Y_test)
    
    train_dataset = TensorDataset(X_train_t, Y_train_t)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    model = get_mtl_model(input_dim=len(MTL_FEATURES))
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Custom loss function to ignore -1 targets
    def mtl_loss(preds, targets):
        loss_fn = nn.BCELoss(reduction='none')
        
        # Mask where target is -1
        mask_h = (targets[:, 0:1] != -1).float()
        mask_d = (targets[:, 1:2] != -1).float()
        mask_s = (targets[:, 2:3] != -1).float()
        
        # Clamp targets to 0-1 range to avoid BCELoss error on -1
        targets_clamped = torch.clamp(targets, min=0.0, max=1.0)
        
        # Calculate loss for all
        losses_h = loss_fn(preds[0], targets_clamped[:, 0:1])
        losses_d = loss_fn(preds[1], targets_clamped[:, 1:2])
        losses_s = loss_fn(preds[2], targets_clamped[:, 2:3])
        
        loss = (losses_h * mask_h).sum() + (losses_d * mask_d).sum() + (losses_s * mask_s).sum()
        total_valid = mask_h.sum() + mask_d.sum() + mask_s.sum()
        
        return loss / (total_valid + 1e-8)

    print("Training MTL model...")
    epochs = 50
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            preds = model(batch_x)
            loss = mtl_loss(preds, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(train_loader):.4f}")
            
    # Save model
    torch.save(model.state_dict(), 'models/multitask/mtl_model.pth')
    
    # Save metadata
    metadata = {
        "model_name": "mediscope_multitask_v1",
        "version": "1.0",
        "features": MTL_FEATURES,
        "diseases": ["heart", "diabetes", "stroke"]
    }
    with open('models/multitask/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("Model trained and saved to models/multitask/mtl_model.pth")

if __name__ == "__main__":
    train_model()
