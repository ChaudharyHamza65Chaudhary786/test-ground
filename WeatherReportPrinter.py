

class WeatherReportPrinter:

    """ A class responsible to print weather reports """

    def print_average_temperatures_month(self, average_values):

        """
        Print AVG Maximum temperature, AVG Minimum temperature and AVG Mean humidity   

        Args:
            average_values : A dictionary containing the average values of max temperature, min temperature, and mean humidity.
 
        """
        print(f"AVG Maximum temperature is: {average_values['Max TemperatureC']} C ")
        print(f"AVG Minimum temperature is: {average_values['Min TemperatureC']} C ")
        print(f"AVG Mean humidity percentage is: {average_values['Mean Humidity']} %")

    def print_temperatures_bar_for_each_record(self, weather_readings):        
        
        """
        Print barchart for temprature ranges of each record   

        Args:
            weather_readings: A list of dictionaries representing weather readings.
        """

        for line_read in weather_readings:                       
            if line_read["Min TemperatureC"] != "":  
                for index in range (int(line_read["Min TemperatureC"])):
                    print("\033[1;34m+", end = " ",)

            if line_read["Max TemperatureC"] != "":
                for index in range (int(line_read["Max TemperatureC"])):
                    print("\033[1;31m+", end = " ",)                                                     

                print(f"\033[1;35m {line_read['Min TemperatureC']} C -"
                    f"{line_read['Max TemperatureC']} C")

    def print_temperatures_year(self, max_temperature, min_temperature, max_humidity):

        """
        prints the maximum and minimum temperatures 
        """
        print(f"highest temperature is: {max_temperature} C ")
        print(f"lowest temperature is: {min_temperature} C ")
        print(f"highest humidity percentage is: {max_humidity} %")
