from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('output2.csv')

y = df.iloc[:, 0].values
X = df.iloc[:, 1:].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = MLPClassifier(hidden_layer_sizes=(500,), activation='relu', solver='adam', alpha=0.0001, max_iter=200, random_state=1)

model.fit(X_train_scaled, y_train)

print("Score de précision sur l'ensemble d'entraînement:", model.score(X_train_scaled, y_train))
print("Score de précision sur l'ensemble de test:", model.score(X_test_scaled, y_test))


