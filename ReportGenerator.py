import WeatherFIleHandler
import WeatherReadingCalculator
import WeatherReportPrinter

class ReportGenerator:

    """ A class that contains handler functions to generate reports """
    
    weather_files_handler = WeatherFIleHandler.WeatherFilesHandler()
    weather_readings_calculator = WeatherReadingCalculator.WeatherReadingsCalculator()
    weather_report_printer = WeatherReportPrinter.WeatherReportPrinter()

    def generate_average_report_handler(self, file_name):

        """
        A function that handles report generation for month by calling necessary functions i.e read file, calculate average and then print report.

        Args:
            file_name = file name against whose report to be genrated

        NOTE : whenever yu want to calculate average for different keys e.g  Mean TempratureC just change average_values dict

        """

        weather_readings = self.weather_files_handler.extract_weather_readings(file_name)
        average_values = {"Max TemperatureC":0 , "Min TemperatureC": 0, "Mean Humidity": 0}
        if  weather_readings: 
            for key in average_values:
                average_values[key] = self.weather_readings_calculator.calculate_average_handler(weather_readings, key)
            self.weather_report_printer.print_average_temperatures_month(average_values)
            

    def generate_barchart_for_file_handler(self, file_name):

        """
        A function that handles report generation for barchart by calling necessary functions i.e read file, then print temprature bars

        Args:
            file_name = file name against whose report to be genrated

        """
        weather_readings = self.weather_files_handler.extract_weather_readings(file_name)
        if weather_readings:
            self.weather_report_printer.print_temperatures_bar_for_each_record(weather_readings)

    def generate_report_for_year_handler(self, files_name):
       
        """
        A function that handles report generation for all files in an year by calling necessary functions i.e read all files for that year, calculate tempratures and print report

        Args:
            files_name : List of all file_names for specified year

        NOTE: whenever want to change keys from Max TemperatureC e.t.c just change names in arguments passed to calculate

        """
        weather_readings = []
        for file_name in files_name:
            weather_readings.extend(self.weather_files_handler.extract_weather_readings(file_name))
  
        max_temp = self.weather_readings_calculator.calculate_max_readings(weather_readings,"Max TemperatureC")
        min_temp = self.weather_readings_calculator.calculate_min_temperatures_yearly(weather_readings,"Min TemperatureC")
        max_humidity = self.weather_readings_calculator.calculate_max_readings(weather_readings,"Max Humidity")
        self.weather_report_printer.print_temperatures_year(max_temp,min_temp,max_humidity)
