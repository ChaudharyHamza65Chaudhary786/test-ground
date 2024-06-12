import argparse
import calendar
import csv
import os
import sys


class TemperatureTracker:

    def __init__(self):       
        self.max_temperature = float('-inf')
        self.max_temperature_date = ""
        self.min_temperature = float('inf')
        self.min_temperature_date = ""
        self.max_humidity = float('-inf')
        self.max_humidity_date = ""
    
    def track_max_temperature(self, temperature, date): 
        if temperature != "":
            self.max_temperature = max(self.max_temperature, int(temperature))
            if self.max_temperature == int(temperature): self.max_temperature_date = date 
        
    def track_min_temperature(self, temperature, date): 
        if temperature != "":
            self.min_temperature = min(self.min_temperature, int(temperature))
            if self.min_temperature == int(temperature): self.min_temperature_date = date

    def track_max_humidity(self, humidity, date):
        if humidity != "":
            self.max_humidity = max(self.max_humidity, int(humidity))
            if self.max_humidity == int(humidity): self.max_humidity_date = date

    def print_temperatures_year(self):
        print(f"highest temperature is: {self.max_temperature} C on {self.max_temperature_date}")
        print(f"lowest temperature is: {self.min_temperature} C on {self.min_temperature_date}")
        print(f"highest humidity percentage is: {self.max_humidity} % on {self.max_humidity_date}")


class WeatherFilesHandler:

    def __open_csv_file(self, file_name):    
        csv_file = open(file_name) 
        return csv_file

    def __read_weather_data_from_csv(self, csv_file, file_name):
        weather_data = list(csv.DictReader(csv_file, skipinitialspace=True))
        if len(weather_data) != 0: return weather_data
        print(f"No Record Found against file : {file_name}")
    
    def return_weather_data(self, file_name):
        csv_file = self.__open_csv_file(file_name)
        weather_data = self.__read_weather_data_from_csv(csv_file, file_name)
        return weather_data

    def return_all_file_names_list_for_year(self, year):
        file_names=[]
        flag = False
        for file_name in os.listdir('.'):
            if year in file_name:
                file_names.append(file_name)
                flag = True
        return file_names if flag else 0
    
    @staticmethod
    def match_and_return_file_name(year, month_name):      
        flag = False    
        for file_name in os.listdir('.'):
            if year in file_name and month_name in file_name:
                return file_name          
        if not flag:     
            print("NO RECORD FOUND AGAINT THIS NAME")
            return False


class WeatherDataCalculator:

    def __calculate_average(self, sum_of_temperature_values, total_number_of_values):    
        for key in sum_of_temperature_values:                           
            sum_of_temperature_values[key] = sum_of_temperature_values[key] / total_number_of_values
        return sum_of_temperature_values

    def __extract_int_value(self, value):
        return int(value) if value != "" else 0
    
    def __calculate_temprature_sum_for_each_record(self, weather_data, sum_of_temperature_values, key): 
        for line_read in weather_data:                                    
                sum_of_temperature_values[key] += self.__extract_int_value(line_read[key])            
        return  sum_of_temperature_values[key]
    
    def calculate_temperature_sum_and_return_average(self, weather_data):
        sum_of_temperature_values = {"Max TemperatureC": 0, "Min TemperatureC": 0, "Mean Humidity": 0}   
        total_records = len(weather_data)
        for key in sum_of_temperature_values:  
            sum_of_temperature_values[key] = self.__calculate_temprature_sum_for_each_record(weather_data, sum_of_temperature_values, key)
        average_values = self.__calculate_average(sum_of_temperature_values, total_records)
    
        return average_values
    

class ReportPrinter:

    def print_average_temperatures_month(self, average_values):
        print(f"AVG Maximum temperature is: {average_values['Max TemperatureC']} C ")
        print(f"AVG Minimum temperature is: {average_values['Min TemperatureC']} C ")
        print(f"AVG Mean humidity percentage is: {average_values['Mean Humidity']} %")

    def print_temperatures_bar_for_each_record(self, weather_data):        
        for line_read in weather_data:                       
            if line_read["Min TemperatureC"] != "":  
                for index in range (int(line_read["Min TemperatureC"])):
                    print("\033[1;34m+", end = " ",)

            if line_read["Max TemperatureC"] != "":
                for index in range (int(line_read["Max TemperatureC"])):
                    print("\033[1;31m+", end = " ",)                                                     

                print(f"\033[1;35m {line_read['Min TemperatureC']} C -"
                    f"{line_read['Max TemperatureC']} C")


class ReportGenerator:
    
    temperature_tracker = TemperatureTracker()
    weather_files_handler = WeatherFilesHandler()
    weather_data_calculator = WeatherDataCalculator()
    report_printer = ReportPrinter()

    def generate_report_for_month_controller(self, file_name):
        weather_data = self.weather_files_handler.return_weather_data(file_name)
        if  weather_data: 
            average_values = self.weather_data_calculator.calculate_temperature_sum_and_return_average(weather_data)
            self.report_printer.print_average_temperatures_month(average_values)

    def generate_barchart_for_file_controller(self, file_name):
        weather_data = self.weather_files_handler.return_weather_data(file_name)
        if weather_data:
            self.report_printer.print_temperatures_bar_for_each_record(weather_data)
    
    def track_tempratures(self,weather_data):
        for line_read in weather_data: 
            self.temperature_tracker.track_min_temperature(line_read["Min TemperatureC"], line_read["PKT"])
            self.temperature_tracker.track_max_temperature(line_read["Max TemperatureC"], line_read["PKT"])
            self.temperature_tracker.track_max_humidity(line_read["Max Humidity"], line_read["PKT"])

    def generate_report_for_year_controller(self, year):
        files_name_list = self.weather_files_handler.return_all_file_names_list_for_year(year)
        for file_name in files_name_list:
             weather_data = self.weather_files_handler.return_weather_data(file_name)
             if weather_data:
                self.track_tempratures(weather_data)                
        self.temperature_tracker.print_temperatures_year()


class CmdArgumentsHandler():

    report_generator = ReportGenerator()

    def validate_year_month(self, year, month_num): 
        return year.isnumeric() and month_num.isnumeric() and int(month_num) in range (1, 13)
    
    def handle_cmd_argument_year(self, year):
        self.report_generator.generate_report_for_year_controller(year)

    def get_year_and_month_from_arguments(self, cmd_argument):
        input = cmd_argument.split('/')                
        input_dict = {"year": input[0], 
                      "month": input[1]}
        return input_dict
    
    def handle_cmd_arguments(self, cmd_argument, key):    
        input_dict = self.get_year_and_month_from_arguments(cmd_argument)
        if self.validate_year_month(input_dict["year"], input_dict["month"]): 

            input_dict["month"] = calendar.month_abbr[int(input_dict["month"])]       
            file_name = WeatherFilesHandler.match_and_return_file_name(input_dict["year"], input_dict["month"])    

            if file_name and key == 'a' :
                self.report_generator.generate_report_for_month_controller(file_name)

            elif file_name and key == 'c' :
                self.report_generator.generate_barchart_for_file_controller(file_name)              
        else: 
            print("INVALID Year or Month Entered")


def main():

    cmd_handler = CmdArgumentsHandler()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help="To print Report for year")
    parser.add_argument('-a', help="To print AVG Report ")
    parser.add_argument('-c', help="To print Barchart Report")
    args = parser.parse_args()

    input_e = args.e
    input_a = args.a
    input_c = args.c

    if input_e : 
        cmd_handler.handle_cmd_argument_year(input_e)
   
    if input_a :
        cmd_handler.handle_cmd_arguments(input_a, "a")
    
    if input_c : 
        cmd_handler.handle_cmd_arguments(input_c, "c")


if __name__ == "__main__":
    main()
