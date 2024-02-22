import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
data_path = "data.csv"
# Define a custom Dataset class
class MyDataset(Dataset):
    def __init__(self, data_path):
    # Read data using pandas
        self.data = pd.read_csv(data_path)
        # Convert features and labels to tensors
        self.features = torch.tensor(self.data.iloc[:, :5].values, dtype=torch.float32)
        self.labels = torch.tensor(self.data["class"], dtype=torch.float32)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        features = self.features[index]
        label = self.labels[index]
        return features, label
    
# Create the dataset instance
dataset = MyDataset(data_path)
# Define batch size and shuffle option
batch_size = 1
shuffle = True
# Create the Dataloader
train_dataloader = DataLoader(dataset,batch_size=batch_size, shuffle=shuffle)