## Notes to understand TensorFlow : 
  - Sequential model is created, which allows you to stack layers linearly
```
model = Sequential() 
```
- A fully connected layer with 8 neurons. input_dim=2 indicates that the input features have 2 dimensions. relu (Rectified Linear Unit) is the activation function used.
```
model.add(Dense(8, input_dim=2, activation='relu')) 
```
- A dropout layer that randomly sets 20% of the input units to 0 at each update during training, which helps prevent overfitting.
```
model.add(Dropout(0.2))
```
-The final layer is a dense layer with 1 neuron, using the sigmoid activation function. This is typical for binary classification, as sigmoid outputs a value between 0 and 1, representing the probability of belonging to one of the classes.
```
model.add(Dense(1, activation='sigmoid'))
```
- The model is compiled with the adam optimizer, a popular choice for deep learning tasks.
The loss function used is binary_crossentropy, appropriate for binary classification.
The metric for performance evaluation is accuracy.
```
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
```
- The model is trained on the input data X and labels y for 1000 epochs. An epoch is a complete pass through the entire training dataset.
```
model.fit(X, y, epochs=1000)
```
- The model's performance is evaluated using the same dataset. It prints out the accuracy of the model.
```
model.fit(X, y, epochs=1000)
```
- Finally, the model makes predictions on the input data X. The output here is the model's predicted probability for each sample belonging to the positive class (label 1).
```
model.fit(X, y, epochs=1000)
```
## Creating a simple model that recognizes sounds

