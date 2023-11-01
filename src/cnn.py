import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from tqdm import tqdm
from torch.functional import F


class TextCNN(nn.Module):
    def __init__(self, len_word, hidden_size, num_classes, dropout=0.5):
        super().__init__()       
        # create a cnn 
        self.conv = nn.ModuleList([nn.Conv1d(in_channels=len_word, out_channels=hidden_size, kernel_size=k, stride=1) for k in [3, 4, 5]])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size*3, num_classes)

    def forward(self, x, hidden):
        #x = torch.unsqueeze(x, dim=1)
        #print(x.shape)

        x.transpose_(1, 2)
        x = [F.relu(conv(x)) for conv in self.conv]
        x = [F.max_pool1d(c, c.size(-1)).squeeze(dim=-1) for c in x]
        x = torch.cat(x, dim=1)
        x = self.dropout(x)
        # requied shape for fc layer
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return torch.sigmoid(x).squeeze()
    
class SequentialCNN(nn.Module):
    def __init__(self, len_word, hidden_size, num_classes, dropout=0.5):
        super().__init__()       
        # create a cnn 
        self.conv1 = nn.Conv1d(in_channels=len_word, out_channels=hidden_size, kernel_size=3)
        self.conv2 = nn.Conv1d(in_channels=hidden_size, out_channels=hidden_size, kernel_size=1)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x, hidden):
        #x = torch.unsqueeze(x, dim=1)
        x.transpose_(1, 2)
        x = F.relu(self.conv1(x))
        x = F.max_pool1d(x, x.size(-1))
        x = F.relu(self.conv2(x))
        x = F.max_pool1d(x, x.size(-1))
        x = self.dropout(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return torch.sigmoid(x).squeeze()