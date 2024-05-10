import torch
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

# User-adjustable parameters
n_estimators = 100  # Default value
learning_rate = 0.1  # Default value
max_depth = 3  # Default value
min_samples_split = 2  # Default value
min_samples_leaf = 1  # Default value
max_features = None  # Default value
subsample = 1.0  # Default value
random_state = 42  # Fixed for reproducibility

'''
n_estimators: int
learning_rate: float
max_depth: int
min_samples_split: int
min_samples_leaf: int
max_features: 'None', 'log2', 'sqrt', or 'auto'
subsample: float

'''

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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)

    # Initialize and train the Gradient Boosting Classifier
    gbc = GradientBoostingClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        subsample=subsample,
        random_state=random_state
    )
    gbc.fit(X_train, y_train)

    # Evaluate the model
    y_pred = gbc.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    avg_accuracy += accuracy

print(f"Average Accuracy: {avg_accuracy / 10:.2f}")
