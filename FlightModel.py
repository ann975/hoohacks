import pandas as pd
import tensorflow as tf
from keras import models, layers #keras is integrated into tensor flow
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

#Read data
data = pd.read_csv('iad_lax_flights.csv')
#print(data.head())

data['Departure Date'] = pd.to_datetime(data['Departure Date'])
data['Departure Timestamp'] = data['Departure Date'].dt.dayofyear

#Preprocessing 
x = data[['Departure Timestamp']].values
y = data['Price'].values

#Scale the features
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

#Reshape the data for LSTM
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

#Building Model - Sequential API used for simpiler linear model
model = models.Sequential(
    [
    #3-layer 
    layers.Dense(64, input_dim=1, activation = "relu", name = "layer1"), #input layer
    layers.Dense(32, activation = "relu", name = "layer2"), 
    layers.Dense(1, name = "predictions")
    ]
)

#Compile Model (optimizer, loss, metrics)
model.compile(
    #Optimizer - Adam to use Stochastic Gradient Descent (SGD) for large datasets
    optimizer="adam",
    # Loss function to minimize
    loss="mse"
)

#Train Model: calling fit()
history = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=500, batch_size=32)

#Evaluate Model
loss = model.evaluate(x_test, y_test)
#print(f"Test Loss: {loss}")

#Generate Prediction
predictions = model.predict(x_test) 
#comparison = pd.DataFrame({'Actual Price': y_test, 'Predicted Price': predictions.flatten()})
#print(comparison)

#Save Model
model.save('flight_price_model.h5')
