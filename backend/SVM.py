import torch
import torch.nn as nn
import torch.optim as optim

class LinearSVM(nn.Module):
    def __init__(self, input_size):
        super(LinearSVM, self).__init__()
        self.fc = nn.Linear(input_size, 1)  # Binary classification

    def forward(self, x):
        h = self.fc(x)
        return h

def train_svm(training_loader, model, epochs, learning_rate, C):
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    for epoch in range(epochs):
        for i, data in enumerate(training_loader, 0):
            inputs, labels = data
            labels[labels == 0] = -1  # Assuming binary labels {0, 1}; SVM needs {-1, 1}
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()  # Remove unnecessary dimensions

            # Hinge loss
            loss = torch.mean(torch.clamp(1 - labels * outputs, min=0))

            # L2 regularization term
            loss += C * torch.mean(model.fc.weight**2)

            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item()}")