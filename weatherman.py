import calendar
import csv
import os
import sys


class TempratureTracker():

    def __init__(self):
        self.max_temprature = float('-inf')
        self.max_temprature_date = ""
        self.min_temprature = float('inf')
        self.min_temprature_date = ""
        self.max_humidity = float('-inf')
        self.max_humidity_date = ""
    
    def update_max_temprature(self, temprature, date):
        self.max_temprature=  temprature
        self.max_temprature_date = date

    def update_min_temprature(self, temprature, date):
        self.min_temprature = temprature
        self.min_temprature_date = date
    
    def update_max_humidity(self, humidity, date):
        self.max_humidity = humidity
        self.max_humidity_date = date
    
    def get_max_temps(self):
        return self.max_temprature, self.min_temprature, self.max_humidity

    def print_tempratures_year(self):
        print(f"highest temprature is: {self.max_temprature} C on {self.max_temprature_date}")
        print(f"lowest temprature is: {self.min_temprature} C on {self.min_temprature_date}")
        print(f"highest humidity percentage is: {self.max_humidity} % on {self.max_humidity_date}")


temprature_tracker = TempratureTracker()


def open_file(file_name):
     
    with open(file_name) as csv_file:
        file_data = list(csv.DictReader(csv_file, skipinitialspace = True))
    return file_data


def file_name_matching_month(year, month_name):                         
    
    flag = False    

    for file_name in os.listdir('.'):
        if year in file_name and month_name in file_name:
            return file_name          
    if not flag :     
        print("NO RECORD FOUND AGAINT THIS NAME")
        return False




def temprature_calculation_whole_month(line_read,sum_of_values_list): 

    if(line_read["Max TemperatureC"] != ""):
               
                sum_of_values_list[0] += int(line_read["Max TemperatureC"])

    if(line_read["Min TemperatureC"] != ""):
               
                sum_of_values_list[1] += int(line_read["Min TemperatureC"])

    if(line_read["Mean Humidity"] != ""):
               
                sum_of_values_list[2] += int(line_read["Mean Humidity"] )

    return sum_of_values_list


def find_average(sum_of_values_list, total_number_of_values):
     
     for index in range (len(sum_of_values_list)):                           
            sum_of_values_list[index] = sum_of_values_list[index] / total_number_of_values
     
     return sum_of_values_list


def print_tempratures_month(average_values_list):
    
    print(f"AVG Highest temprature is: {average_values_list[0]} C ")
    print(f"AVG Lowest temprature is: {average_values_list[1]} C ")
    print(f"AVG Mean humidity percentage is: {average_values_list[2]} %")

    
def generate_report_for_month(file_name):
    
    sum_of_values_list = [0, 0, 0]  
    total_lines = 1
    file_data = open_file(file_name)

    for line_read in file_data:                   
        sum_of_values_list = temprature_calculation_whole_month(line_read, sum_of_values_list)
        total_lines += 1

    average_values_list = find_average(sum_of_values_list, total_lines-1)
    print_tempratures_month(average_values_list)




def print_tempratures_bar(temprature_calculation_dict):  

    for index in range (temprature_calculation_dict["lowest_temprature_on_highest_day"]):
         print("\033[1;34m+", end = " ",)

    for index in range (temprature_calculation_dict["highest_temprature_month"]):
         print("\033[1;31m+", end = " ",)                                                                 

    print(f"\033[1;35m {temprature_calculation_dict['lowest_temprature_on_highest_day']} C - 
          {temprature_calculation_dict['highest_temprature_month']} C")                   

    print("\n")

    for index in range (temprature_calculation_dict["lowest_temprature_month"]):
         print("\033[1;34m+", end = " ",)

    for index in range (temprature_calculation_dict["highest_temprature_on_lowest_day"]):
         print("\033[1;31m+", end = " ",)       
                                                                          
    print(f"\033[1;35m {temprature_calculation_dict['lowest_temprature_month']} C - 
          {temprature_calculation_dict['highest_temprature_on_lowest_day']} C \033[0m")


def generate_barchart_for_file(file_name):

    temprature_calculation_dic = { 
        "highest_temprature_month": float("-inf"),
        "highest_temprature_on_lowest_day": float("-inf"),
        "lowest_temprature_month": float("inf"), 
        "lowest_temprature_on_highest_day": float("inf")
    }
    file_data = open_file(file_name)
    
    for line_read in file_data:                         
        temprature_calculation_dic = temprature_calculation_barchart(line_read,temprature_calculation_dic)

    print_tempratures_bar(temprature_calculation_dic)


def temprature_calculation_barchart(line_read,temprature_calculation_dict):
    
    if(line_read["Max TemperatureC"] != ""  and 
         int(line_read["Max TemperatureC"]) > temprature_calculation_dict["highest_temprature_month"]  ):    
               
            temprature_calculation_dict["highest_temprature_month"] = int(line_read["Max TemperatureC"])
            temprature_calculation_dict["lowest_temprature_on_highest_day"] = int(line_read["Min TemperatureC"])
                        
    if(line_read["Min TemperatureC"] != "" and 
            int(line_read["Min TemperatureC"]) < temprature_calculation_dict["lowest_temprature_month"] ):        
                                                                    
                temprature_calculation_dict["lowest_temprature_month"] = int(line_read["Min TemperatureC"])
                temprature_calculation_dict["highest_temprature_on_lowest_day"] = int(line_read["Max TemperatureC"])    
    
    return temprature_calculation_dict




def files_traversal_year(year):

        flag = False 
        for file_name in os.listdir('.'):
            if year in file_name:
                generate_report_year(file_name)
                flag = True

        return flag


def temprature_calculation_year(line_read):

    highest_temprature, lowest_temprature, highest_humidity = temprature_tracker.get_max_temps()

    if (line_read["Min TemperatureC"] != "" and 
        int(line_read["Min TemperatureC"]) < lowest_temprature): 
                                                
        temprature_tracker.update_min_temprature(int(line_read['Min TemperatureC' ]),
                                      line_read["PKT"])

    if(line_read["Max TemperatureC"]!= ""  and 
        int(line_read["Max TemperatureC"]) > highest_temprature):   
        
        temprature_tracker.update_max_temprature(int(line_read["Max TemperatureC"]),
                                      line_read["PKT"]) 

    if(line_read["Max Humidity"]!= "" and 
        int(line_read["Max Humidity"]) > highest_humidity):

        temprature_tracker.update_max_humidity(int(line_read["Max Humidity"]),
                                          line_read["PKT"])    


def generate_report_year(file_name):  

    file_data = open_file(file_name)
    for line_read in file_data: 
        temprature_calculation_year(line_read)      




def validate_year_month(year, month_num):
     
     if year.isnumeric() and month_num.isnumeric() and int(month_num) in range (1, 13):       
          return True
     else:
          return False


def handle_cmd_arguments(cmd_argumentList, index):

        values = cmd_argumentList[index+1].split('/')                
        year = values[0] 
        month_num = values[1]
       
        if "/" in cmd_argumentList[index+1] and validate_year_month(year, month_num):
            
            month_name = calendar.month_abbr[int(month_num)]       
            file_name = file_name_matching_month(year, month_name) 

            if file_name != False and cmd_argumentList[index] == '-a' :

                generate_report_for_month(file_name)

            elif file_name != False and cmd_argumentList[index] == '-c' :
                generate_barchart_for_file(file_name)                    

        else: 
            print("INVALID Year or Month Entered")
     
 
def main():

    cmd_argumentList = sys.argv[1:]      

    for index in  range (len(cmd_argumentList)):

        if cmd_argumentList[index] == '-e':
            
            year = cmd_argumentList[index+1]

            if files_traversal_year(year) == False:                       
                print(f" File  Not Found for year {year}")
            else:
                temprature_tracker.print_tempratures_year()

        if cmd_argumentList[index] == '-a' or cmd_argumentList[index] == '-c':           
            handle_cmd_arguments(cmd_argumentList, index)            


if __name__ == "__main__":
    main()

