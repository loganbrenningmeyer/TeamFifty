import torch
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

# Load your PyTorch tensors
input_data = torch.load('input_data.pt')
target_data = torch.load('target_data.pt')

avg_accuracy = 0

for i in range(10):
    # Shuffle the data
    shuffle = torch.randperm(input_data.shape[0])
    input_data = input_data[shuffle]
    target_data = target_data[shuffle]

    # Convert PyTorch tensors to NumPy arrays
    X = input_data.numpy()
    y = target_data.numpy()

    # Split the data into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train the Gradient Boosting Classifier
    gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    gbc.fit(X_train, y_train)

    # Evaluate the model
    y_pred = gbc.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    avg_accuracy += accuracy

print(f"Average Accuracy: {avg_accuracy / 10:.2f}")