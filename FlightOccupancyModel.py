import pandas as pd
import tensorflow as tf
from keras import models, layers, optimizers #keras is integrated into tensor flow
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

#Read data
data = pd.read_csv('filtered_flights.csv')
#print(data.head())

#Clean data - remove any incosistencies in the data
data = data.dropna()
data = data.replace([np.inf, -np.inf], np.nan).dropna()
data = data[data['Seats'] > 0]

#Convert Fly_date to datetime format and create new columns
data['Fly_date'] = pd.to_datetime(data['Fly_date'])
data['date timestamp'] = data['Fly_date'].dt.dayofyear
#Create a new column for calculated occupancy of the flight
data['occupancy'] = (data['Passengers'] / data['Seats']) * 100


#Preprocessing 
x = data[['date timestamp']].values
y = data['occupancy'].values

#check file for any NaN or infinite values
#print(y)
#print(np.isnan(y).sum())  # Check for NaN values
#print(np.isinf(y).sum())  # Check for infinite values

#Scale the features
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

#Split the data into training and testing sets: 80% testing, 20% testing
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
    optimizer=optimizers.Adam(learning_rate=0.001),
    # Loss function to minimize
    loss="mse",
    metrics=["mae", "mse"]
)

#Train Model: calling fit(), process the data 300 times, batch size of 64
history = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=300, batch_size=64)

#Evaluate Model
loss = model.evaluate(x_test, y_test)
#print(f"Test Loss: {loss}")

#Generate Prediction
predictions = model.predict(x_test) 
comparison = pd.DataFrame({'Actual Occupancy': y_test, 'Predicted Occupany': predictions.flatten()})
print(comparison)

#Save Model
model.save('flight_occupancy_model.h5')

#Prompt for Input
date = input("Please enter a date (YYYY-MM-DD): ")
while not isinstance(date, str) or len(date) != 10:
    date = input("Invalid date format. Please enter a date (YYYY-MM-DD): ")
datetimeformat = pd.to_datetime(date)
day_of_year = datetimeformat.dayofyear
day_of_year_reshaped = np.array([[day_of_year]])
input_data_scaled = scaler.fit_transform(day_of_year_reshaped)
prediction = model.predict(input_data_scaled)[0][0]
print(f"Predicted occupancy for {date}: {prediction:.2f}%")

