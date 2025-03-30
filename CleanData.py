import pandas as pd
# function that fliter flight data to only include flights from a specific origin to a specific destinatio
def filter_flight_data(dataframe, origin_airport, destination_airport, output_file):
    filtered_data = dataframe[
        (dataframe['Origin_airport'] == origin_airport) &
        (dataframe['Destination_airport'] == destination_airport)
    ]
    filtered_data.to_csv(output_file, index=False) #prints the filtered data to a csv file
    #print(f"Filtered data saved to {output_file}") 

# Example usage:
df = pd.read_csv('Airports2.csv')  # Load your dataset
filter_flight_data(df, 'DCA', 'LAX', 'filtered_flights.csv') #calls the function to filter the data