
import calendar
import fnmatch
import os
import sys


class temprature_Tracker():

    def __init__(self):
        self.max_temp = float('-inf')
        self.max_temp_date = ""
        self.min_temp = float('inf')
        self.min_temp_date = ""
        self.max_humidity = float('-inf')
        self.max_humidity_date = ""
    
    def update_max_temp(self, mx_temp, mx_date):
        self.max_temp = mx_temp
        self.max_temp_date = mx_date

    def update_min_temp(self, mn_temp, mn_date):
        self.min_temp = mn_temp
        self.min_temp_date = mn_date
    
    def update_max_humidity(self, mx_humidity, mx_date):
        self.max_humidity = mx_humidity
        self.max_humidity_date = mx_date
    
    def get_max_temps(self):
        return self.max_temp, self.min_temp, self.max_humidity

    def print_tempratures_year(self):
        print(f"highest temp is: {self.max_temp} C on {self.max_temp_date}")
        print(f"lowest temp is: {self.min_temp} C on {self.min_temp_date}")
        print(f"highest humidity percentage is: {self.max_humidity} % on {self.max_humidity_date}")

temp_tracker = temprature_Tracker()
        

def file_name_matching_month(year, month_name):                         

     for file_name in os.listdir('.'):
        if year in file_name and month_name in file_name:
            return file_name
        
     print("NO RECORD FOUND AGAINT THIS NAME")
     return False


def file_name_matching(year):          

    flag = False
    for file_name in os.listdir('.'):
        if year in file_name:
            file_parsing_year(file_name)
            flag = True
    if flag:
        temp_tracker.print_tempratures_year()
    else:
        return False


def file_parsing_year(file_name):  

    coloumn_indexes_dict = {}
    file_ope = open(file_name, "r") 
    start_reading = False
    file_open = open(file_name, "r")
    total_lines = 1
    lines = file_open.readlines()                 

    
    for line in lines: 

        if start_reading == False and "Max TemperatureC" and "Min TemperatureC" and "Max Humidity" in line:
            coloums_name_list = file_ope.readlines()[total_lines-1].strip().split(',') 

            for i in range(len(coloums_name_list)):       
                coloumn_indexes_dict[coloums_name_list[i]]=i
            
            start_reading = True
            file_ope.close()
            continue

        if start_reading: 
            values = line.strip().split(',')    
            highest_temp, lowest_temp, highest_humidity = temp_tracker.get_max_temps()

            if (values[coloumn_indexes_dict["Min TemperatureC"]] != "" and 
                int(values[coloumn_indexes_dict["Min TemperatureC"]]) < lowest_temp): 
                                                        
                temp_tracker.update_min_temp(int(values[coloumn_indexes_dict['Min TemperatureC' ]]), values[coloumn_indexes_dict["PKT"]])

            if(values[coloumn_indexes_dict["Max TemperatureC"]] != ""  and 
               int(values[coloumn_indexes_dict["Max TemperatureC"]]) > highest_temp):   
                
                temp_tracker.update_max_temp( int(values[coloumn_indexes_dict["Max TemperatureC"]]), values[coloumn_indexes_dict["PKT"]]) 

            if(values[coloumn_indexes_dict["Max Humidity"]] != "" and 
               int(values[coloumn_indexes_dict["Max Humidity"]]) > highest_humidity):

                temp_tracker.update_max_humidity(int(values[coloumn_indexes_dict["Max Humidity"]]), values[coloumn_indexes_dict["PKT"]])

        total_lines += 1
            
    file_open.close()
    


def file_parsing_month(file_name):

    coloumn_indexes_dict = {}
    average_values = [0, 0, 0]                                         
    file_open = open(file_name,"r")
    file_ope = open(file_name, "r")
    lines = file_open.readlines()
    start_reading = False
    total_lines = 1
    
    for line in lines:                   

        if (start_reading == False and 
           "Max TemperatureC" and "Min TemperatureC" and " Mean Humidity" in line):
        
                coloums_name_list = file_ope.readlines()[total_lines-1].strip().split(',')

                for i in range(len(coloums_name_list)):       
                    coloumn_indexes_dict[coloums_name_list[i]] = i
                
                start_reading = True
                file_ope.close()
                continue
        
        if start_reading: 
            values = line.strip().split(',')      

            if(values[coloumn_indexes_dict ["Max TemperatureC"]] != "" and 
               int(values[coloumn_indexes_dict["Max TemperatureC"]].isnumeric())):
               
                average_values[0] += int(values[coloumn_indexes_dict["Max TemperatureC"]])

            if(values[coloumn_indexes_dict ["Min TemperatureC"]] != "" and 
               int(values[coloumn_indexes_dict["Min TemperatureC"]].isnumeric())):
               
                average_values[1] += int(values[coloumn_indexes_dict["Min TemperatureC"]])

            if(values[coloumn_indexes_dict [" Mean Humidity"]] != "" and 
               int(values[coloumn_indexes_dict  [" Mean Humidity"]].isnumeric())):
               
                average_values[2] += int(values[coloumn_indexes_dict[" Mean Humidity"]] )
        
        total_lines += 1 
   
    if start_reading:
        for i in range (len(average_values)):                           
            average_values[i] = average_values[i] / total_lines

        print_tempratures_month(average_values)

    else:       
        print(f" NO DATA FOUND IN FILE {file_name}")     

    file_open.close()




def file_parsing_barchart(file_name):
    
    coloumn_indexes_dict = {}
    highest_temp_month = float("-inf")
    highest_temp_on_lowest_day = float("-inf")
    lowest_temp_month = float("inf")
    lowest_temp_on_highest_day = float("inf")
    start_reading = False
    total_lines = 1
    
    file_open = open(file_name, "r")
    file_ope = open(file_name, "r")
    lines = file_open.readlines()  
 
    for line in lines:              

        if start_reading == False and "Max TemperatureC" and "Min TemperatureC"  in line:

            coloums_name_list = file_ope.readlines()[total_lines-1].strip().split(',')

            for i in range(len(coloums_name_list)):       
                coloumn_indexes_dict[coloums_name_list[i]] = i
            
                start_reading = True
                file_ope.close()
            continue
              
        if start_reading:            

            values = line.strip().split(',')  
            if(values[coloumn_indexes_dict["Max TemperatureC"]] != ""  and 
               int(values[coloumn_indexes_dict["Max TemperatureC"]]) > highest_temp_month  ):    
               
                highest_temp_month = int(values[coloumn_indexes_dict["Max TemperatureC"]])
                lowest_temp_on_highest_day = int(values[coloumn_indexes_dict["Min TemperatureC"]])
                        
            if(values[coloumn_indexes_dict["Min TemperatureC"]] != "" and 
               int(values[coloumn_indexes_dict["Min TemperatureC"]]) < lowest_temp_month ):        
                                                                    
                lowest_temp_month = int(values[coloumn_indexes_dict["Min TemperatureC"]])
                highest_temp_on_lowest_day = int(values[coloumn_indexes_dict["Max TemperatureC"]])

        total_lines += 1

    print_tempratures_bar(highest_temp_month, lowest_temp_on_highest_day, lowest_temp_month, highest_temp_on_lowest_day)

         


def print_tempratures_bar(highest_temp_month, lowest_temp_on_highest_day, lowest_temp_month, highest_temp_on_lowest_day):  

    for i in range (lowest_temp_on_highest_day):
         print("\033[1;34m+", end = " ",)

    for i in range (highest_temp_month):
         print("\033[1;31m+", end = " ",)                                                                 

    print(f"\033[1;35m {lowest_temp_on_highest_day} C - {highest_temp_month} C")                   

    print("\n")

    for i in range (lowest_temp_month):
         print("\033[1;34m+", end = " ",)

    for i in range (highest_temp_on_lowest_day):
         print("\033[1;31m+", end = " ",)       
                                                                          
    print(f"\033[1;35m {lowest_temp_month} C - {highest_temp_on_lowest_day} C")                      

def print_tempratures_month(average_values):

    
    print(f"AVG Highest temp is: {average_values[0]} C ")
    print(f"AVG Lowest temp is: {average_values[1]} C ")
    print(f"AVG Mean humidity percentage is: {average_values[2]} %")




def main():

    cmd_argumentList = sys.argv[1:]                              
    
    for i in  range (len(cmd_argumentList)):


        if cmd_argumentList[i] == '-e':
            print("\n")
            year = cmd_argumentList[i+1]
            if(file_name_matching(year) != False ):                       
                print("\033[1;32m---------------------------------------------"
                      "-------------------------------------\033[0m", end = "")
            else: 
                print(f" File  Not Found for year {year}")

        if cmd_argumentList[i] == '-a':            
            if "/" in cmd_argumentList[i+1]:
                values = cmd_argumentList[i+1].split('/')                
                year = values[0] 

                if  values[0].isnumeric() and values[1].isnumeric() and int(values[1]) in range (1,12):
                    month_name = calendar.month_abbr[int(values[1])]       
                    file_name = file_name_matching_month(year, month_name) 
                    if file_name != False:
                        print(f"\n\nData for {year, month_name} \n")
                        file_parsing_month(file_name)
                        print("\033[1;32m--------------------------------------"
                              "--------------------------------------------\033[0m", end = "")
                else: 
                    print("INVALID Year or Month Entered")
            else: 
                print(" Invalid Input")

        if cmd_argumentList[i] == '-c':
            if "/" in cmd_argumentList[i+1]:
                values = cmd_argumentList[i+1].split('/')               
                year = values[0] 

                if  values[0].isnumeric() and values[1].isnumeric() and int(values[1]) in range (1, 12):
                    month_name = calendar.month_abbr[int(values[1])]       
                    file_name = file_name_matching_month(year,month_name) 
                    if file_name != False:
                        print(f"\n\nBar Chart for {year,month_name} \n")
                        file_parsing_barchart(file_name)
                        print("\033[1;32m----------------------------------------------------------------------------------\033[0m", end="")
                        print("\n")
                else: 
                    print("INVALID Year or Month Entered")
            else: 
                print(" Invalid Input")




if __name__ == "__main__":
    main()


