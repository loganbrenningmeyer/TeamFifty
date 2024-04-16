import numpy as np
import torch
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load the data (assuming it's been preprocessed and saved as torch tensors)
input_data_2022 = torch.load(f"input_data_1_2022.pt").numpy()
target_data_2022 = torch.load(f"target_data_1_2022.pt").numpy().ravel()

input_data_2023 = torch.load(f"input_data_1_2023.pt").numpy()
target_data_2023 = torch.load(f"target_data_1_2023.pt").numpy().ravel()

input_data = np.concatenate((input_data_2022, input_data_2023), axis=0)
target_data = np.concatenate((target_data_2022, target_data_2023), axis=0)

# Normalize the data
scaler = StandardScaler()
input_data = scaler.fit_transform(input_data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(input_data, target_data, test_size=0.2, random_state=42)

# Initialize the SVM classifier
clf = svm.SVC(kernel='rbf', C=1.0, gamma='auto')  # RBF Kernel, you can tune these hyperparameters

# Train the SVM classifier
clf.fit(X_train, y_train)

# Predict the labels on the test set
y_pred = clf.predict(X_test)

# Print out the performance metrics
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# Additionally print out predictions vs actuals for insights
for pred, actual in zip(y_pred, y_test):
    print(f"Prediction: {pred}, Actual: {actual}")
