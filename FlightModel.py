import pandas as pd
import tensorflow as tf
from keras import models, layers #keras is integrated into tensor flow
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

#Read data
data = pd.read_csv('iad_lax_flights.csv')
print(data.head())

data['Departure Date'] = pd.to_datetime(data['Departure Date'])
data['Departure Timestamp'] = data['Departure Date'].dt.dayofyear

features = ['Flight ID','Departure Airport','Arrival Airport','Departure Timestamp']
target = 'Price'

label_encoder = LabelEncoder()
data['Flight ID'] = label_encoder.fit_transform(data['Flight ID'])
data['Departure Airport'] = label_encoder.fit_transform(data['Departure Airport'])
data['Arrival Airport'] = label_encoder.fit_transform(data['Arrival Airport'])
data['Departure Timestamp'] = label_encoder.fit_transform(data['Departure Timestamp'])



#Preprocessing 
x = data[features]
y = data[target]

#Scale the features
scaler = StandardScaler()
#x_scaled = scaler.fit_transform(x)

#Reshape the data for LSTM
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))

#Building Model - Sequential API used for simpiler linear model
model = models.Sequential(
    [
    #3-layer 
    layers.Input(shape=(x_train.shape[1], x_train.shape[2]), name = "input"), 
    layers.Dense(64, activation = "relu", name = "layer1"),
    layers.Dense(32, activation = "relu", name = "layer2"), 
    layers.Dense(1, name = "predictions")
    ]
)

#Compile Model (optimizer, loss, metrics)
model.compile(
    #Optimizer - Adam to use Stochastic Gradient Descent (SGD) for large datasets
    optimizer="adam",
    # Loss function to minimize
    loss="mse",
    # List of metrics to monitor
    metrics=["mae"]
)

#Train Model: calling fit()
model.fit(x_train, y_train, validation_data = (x_test, y_test))

#Evaluate Model
model.evaluate(x_test, y_test)

#Generate Prediction
predictions = model.predict(x_test) 
comparison = pd.DataFrame({'Actual Price': y_test, 'Predicted Price': predictions.flatten()})
print(comparison)


#Save Model
model.save('flight_price_model.h5')