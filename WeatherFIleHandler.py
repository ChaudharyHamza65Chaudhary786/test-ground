import csv
import os

class WeatherFilesHandler:

    """
    This class is responsible of handling files i.e matching file_names, opening them and exctracting data from it.
    """

    def __open_csv_file(self, file_name):   

        """ Takes in the file name and opens it """

        return open(file_name) 

    def __read_weather_readings_from_csv(self, csv_file, file_name):

        """
        Read weather readings from a CSV file.

        Args:
            csv_file : The CSV file object to read from.
            file_name: The name of the CSV file.

        Returns:
            list: A list of dictionaries representing weather readings.

        Prints a message if CSV file is empty.
        """
        
        weather_readings = list(csv.DictReader(csv_file, skipinitialspace=True))
        if len(weather_readings) != 0: 
            return weather_readings
        print(f"No Record Found against file : {file_name}")
    
    def extract_weather_readings(self, file_name):
        
        """
        A handler function that calls other functions to open and read file

        Args:
            file_name: The name of the CSV file.

        Returns:
            list: A list of dictionaries representing weather readings.

        """

        csv_file = self.__open_csv_file(file_name)
        weather_readings = self.__read_weather_readings_from_csv(csv_file, file_name)
        return weather_readings
    
    def match_and_extract_file_name(self, year, month_name=0):
        
        """
        Search for weather files based on given year and optional month
        files are store like 2004-aug.txt

        Args: 
            year: The year for which weather data is required.
            month_name: Month for which data is required
        
        Returns:
            If month_name is provided and a file matching both year and month is found, returns the name of the file.
            If month_name is not provided, returns a list of all file names for that particular year
        
        """
        weather_file_names = []
        flag = False
        if month_name:
            for file_name in os.listdir('.'):
                if year in file_name and month_name in file_name:
                    return file_name
        else:
            for file_name in os.listdir('.'):
                if year in file_name:
                    weather_file_names.append(file_name)
                    flag = True
            return weather_file_names       
        if not flag:     
            print("NO RECORD FOUND AGAINT THIS NAME")
            return False
