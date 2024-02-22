import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from torch import optim
from tqdm import tqdm
import matplotlib.pyplot as plt
import os

torch.manual_seed(0)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, output):
        super(NeuralNet, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, output)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.sigmoid(out)
        return out
    
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
    
    
input_size = 5
hidden_size = 3
output = 1
model = NeuralNet(input_size,hidden_size,output)

input_X = torch.from_numpy(np.array([1, 0.1, 0.4, -0.2, -1])).float()
output = model.forward(input_X)
print(output)
output = torch.where(output > 0.5, 1, 0)
print(output)
print(output.item())

data_path = "data.csv"
    
# Create the dataset instance
dataset = MyDataset(data_path)
# Define batch size and shuffle option
batch_size = 1
shuffle = True
# Create the Dataloader
train_dataloader = DataLoader(dataset,batch_size=batch_size, shuffle=shuffle)

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
num_epochs = 20
learning_rate = 0.001
model = NeuralNet(input_size, hidden_size, output)
optimizer = optim.SGD(model.parameters(), lr=learning_rate)
loss_func = torch.nn.BCELoss()
loss_epoch = {}
loss_values = []

for epoch in tqdm(range(num_epochs)):
    for X, y in train_dataloader:
        # zero the parameter gradients
        optimizer.zero_grad()
        # forward + backward + optimize
        pred = model(X)
        loss = loss_func(pred, y.unsqueeze(1))
        loss_values.append(loss.item())
        loss.backward()
        optimizer.step()
        loss_epoch[epoch] = sum(loss_values) / len(loss_values)

plt.plot(loss_epoch.keys(), loss_epoch.values(), 'r--')
plt.legend(['Training Loss'])
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()