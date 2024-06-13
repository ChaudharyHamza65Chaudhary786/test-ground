

class WeatherReadingsCalculator:
    
    """
    A class to perform calculations on weather data. All methods are independent, just type the key, i.e what reading you want, in argument and calculate_functions would work on key if it exists. 
    e.g max function would work on all keys like max_temp, min_temp, lowest humidity e.t.c
    """

    def __calculate_average(self, sum_of_temperature_values, total_number_of_values):    

        """
        A function that calculates average and returns it

        Args:
            sum_of_temperature_values = contains sum of key for whole fole
            total_number_of_values = total readings available for month

        Returns:
            average of temperature value

        """
        return  sum_of_temperature_values / total_number_of_values

    def __extract_int_value(self, value):
        """
        convert temprature reading to int from str if reading is not empty
        """
        return int(value) if value != "" else 0
    
    def __calculate_temprature_sum_for_each_record(self, weather_readings, key): 

        """
        A function that sums the temprature reading and returns it

        Args:
            weather_reading = list of dictionary that contains weather readings for a file
            key: Maximum temp, Minimum Temp or Mean humidity. Any temprature record

        Returns:
            sum of temprature value for a month
        """
        sum_of_temperature_values = 0
        for line_read in weather_readings:                                    
            sum_of_temperature_values += self.__extract_int_value(line_read[key])            
        return sum_of_temperature_values
    
    def calculate_average_handler(self, weather_readings, key):
        
        """
        A  function that handles the calculation of average values of given key
         
        Args:
            weather_reading = list of dictionary that contains weather readings for a file
            key: Maximum temp, Minimum Temp or Mean humidity. Any temprature record

        
        Returns:
           average of temprature value
        
        """
        total_records = len(weather_readings)
        sum_of_temperature_values = self.__calculate_temprature_sum_for_each_record(weather_readings, key)
        average_values = self.__calculate_average(sum_of_temperature_values, total_records)

        return average_values
    
    def get_temperatures(self, weather_readings, key):

        """
        Extracts temperatures from a list of weather readings based on the provided key.

        Args:
            weather_readings (list): A list of dictionaries representing weather readings.
            key: Maximum temp, Minimum Temp or Mean humidity. Any temprature record

        Returns:
            list: A list of temperature values extracted from the weather readings.

        """
        temperature_list = []
        for record in weather_readings:
            if record[key] != "":
                temperature_list.append(int(record[key]))
        return temperature_list

    def calculate_max_readings(self, weather_readings, key):     
        
        """
        Calculate the maximum reading based on key. e.g maximum temp, mean humidity, max wind from weather_readings

        Args:
            weather_readings: A list of dictionary containing weather readings.
            key: Maximum temp, Minimum Temp or Mean humidity. Any temprature record

        Returns:
            The maximum Reading.
        """  
        return  max(self.get_temperatures(weather_readings,key))
    
    def calculate_min_temperatures_yearly(self, weather_readings, key):   

        """
        Calculate the minimum reading based on key. e.g min temp, minimum mean humidity, min highest temp from weather_readings

        Args:
            weather_readings: A list of dictionary containing weather readings.
            key: Maximum temp, Minimum Temp or Mean humidity. Any temprature record

        Returns:
            The minimimum Reading.
        """  
        return  min(self.get_temperatures(weather_readings,key))
