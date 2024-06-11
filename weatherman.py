import calendar
import csv
import os
import sys


class temperatureTracker():

    def __init__(self):       
        self.max_temperature = float('-inf')
        self.max_temperature_date = ""
        self.min_temperature = float('inf')
        self.min_temperature_date = ""
        self.max_humidity = float('-inf')
        self.max_humidity_date = ""
    
    def set_max_temperature(self, temperature, date):
        self.max_temperature = temperature
        self.max_temperature_date = date

    def set_min_temperature(self, temperature, date):
        self.min_temperature = temperature
        self.min_temperature_date = date
    
    def set_max_humidity(self, humidity, date):
        self.max_humidity = humidity
        self.max_humidity_date = date
    
    def get_max_temps(self):
        return self.max_temperature, self.min_temperature, self.max_humidity

    def print_temperatures_year(self):
        print(f"highest temperature is: {self.max_temperature} C on {self.max_temperature_date}")
        print(f"lowest temperature is: {self.min_temperature} C on {self.min_temperature_date}")
        print(f"highest humidity percentage is: {self.max_humidity} % on {self.max_humidity_date}")


temperature_tracker = temperatureTracker()


def open_csv_file(file_name):    
    csv_file = open(file_name) 
    return csv_file


def read_weather_data_from_csv(csv_file):
    weather_data = list(csv.DictReader(csv_file, skipinitialspace=True))
    if len(weather_data) == 0:
        return False
    return weather_data


def match_file_name(year, month_name):                            
    flag = False    
    for file_name in os.listdir('.'):
        if year in file_name and month_name in file_name:
            return file_name          
    if not flag:     
        print("NO RECORD FOUND AGAINT THIS NAME")
        return False


def extract_int_value(value): return int(value) if value != "" else 0


def calculate_temprature_sum_for_each_record(weather_data): 
    sum_of_temperature_values = {"max_temperature": 0, "min_temperature": 0, "mean_humidity": 0}   
    for line_read in weather_data:                                    
            sum_of_temperature_values["max_temperature"] += extract_int_value(line_read["Max TemperatureC"])            
            sum_of_temperature_values["min_temperature"] += extract_int_value(line_read["Min TemperatureC"])
            sum_of_temperature_values["mean_humidity"] += extract_int_value(line_read["Mean Humidity"] )
    return  sum_of_temperature_values


def calculate_average(sum_of_temperature_values, total_number_of_values):    
    for key in sum_of_temperature_values:                           
        sum_of_temperature_values[key] = sum_of_temperature_values[key] / total_number_of_values
    return sum_of_temperature_values


def print_temperatures_month(average_values):
    print(f"AVG Maximum temperature is: {average_values['max_temperature']} C ")
    print(f"AVG Minimum temperature is: {average_values['min_temperature']} C ")
    print(f"AVG Mean humidity percentage is: {average_values['mean_humidity']} %")

    
def generate_report_for_month_controller(file_name):   
    csv_file = open_csv_file(file_name)
    weather_data = read_weather_data_from_csv(csv_file)
    total_records = len(weather_data)
    if weather_data == 0 : 
        print(file_name, "File Empty")
    else:
        sum_of_temperature_values = calculate_temprature_sum_for_each_record(weather_data)
        average_values = calculate_average(sum_of_temperature_values, total_records)
        print_temperatures_month(average_values)


def print_temperatures_bar_for_each_record(weather_data):
    for line_read in weather_data:                       

        if line_read["Min TemperatureC"] != "":  
            for index in range (int(line_read["Min TemperatureC"])):
                print("\033[1;34m+", end = " ",)

        if line_read["Max TemperatureC"] != "":
            for index in range (int(line_read["Max TemperatureC"])):
                print("\033[1;31m+", end = " ",)                                                     

            print(f"\033[1;35m {line_read['Min TemperatureC']} C -"
                f"{line_read['Max TemperatureC']} C")


def generate_barchart_for_file_controller(file_name):
    csv_file = open_csv_file(file_name)
    weather_data = read_weather_data_from_csv(csv_file)   
    if weather_data == 0:
        print(file_name, "File Empty")
    else:
        print_temperatures_bar_for_each_record(weather_data)


def traverse_files_of_same_year(year):
    flag = False 
    for file_name in os.listdir('.'):
        if year in file_name:
            generate_report_year_controller(file_name)
            flag = True
    return flag


def update_yearly_temperature(line_read):
    highest_temperature, lowest_temperature, highest_humidity = temperature_tracker.get_max_temps()   
    if(line_read["Min TemperatureC"] != "" and int(line_read["Min TemperatureC"]) < lowest_temperature):        
        temperature_tracker.set_min_temperature(int(line_read['Min TemperatureC' ]), line_read["PKT"])

    if(line_read["Max TemperatureC"] != ""  and int(line_read["Max TemperatureC"]) > highest_temperature): 
        temperature_tracker.set_max_temperature(int(line_read["Max TemperatureC"]), line_read["PKT"]) 
        
    if(line_read["Max Humidity"] != "" and int(line_read["Max Humidity"]) > highest_humidity):
        temperature_tracker.set_max_humidity(int(line_read["Max Humidity"]), line_read["PKT"])    


def generate_report_year_controller(file_name):  
    csv_file = open_csv_file(file_name)
    weather_data = read_weather_data_from_csv(csv_file)
    if weather_data == 0:
        print(file_name, "File Empty")
    else:
        for line_read in weather_data: 
            update_yearly_temperature(line_read)      


def validate_year_month(year, month_num): return year.isnumeric() and month_num.isnumeric() and int(month_num) in range (1, 13)


def handle_cmd_arguments(cmd_argumentList, index):
        cmd_argument = cmd_argumentList[index+1].split('/')                
        year = cmd_argument[0] 
        month_num = cmd_argument[1]

        if "/" in cmd_argumentList[index+1] and validate_year_month(year, month_num):           
            month_name = calendar.month_abbr[int(month_num)]       
            file_name = match_file_name(year, month_name) 

            if file_name != False and cmd_argumentList[index] == '-a' :
                generate_report_for_month_controller(file_name)

            elif file_name != False and cmd_argumentList[index] == '-c' :
                generate_barchart_for_file_controller(file_name)              
        else: 
            print("INVALID Year or Month Entered")


def main():
    cmd_argumentList = sys.argv[1:]      
    for index in  range (len(cmd_argumentList)):
        if cmd_argumentList[index] == '-e':            
            year = cmd_argumentList[index+1]
            if traverse_files_of_same_year(year) == False:                       
                print(f" File  Not Found for year {year}")
            else:
                temperature_tracker.print_temperatures_year()
        if cmd_argumentList[index] == '-a' or cmd_argumentList[index] == '-c':           
            handle_cmd_arguments(cmd_argumentList, index)            


if __name__ == "__main__":
    main()
