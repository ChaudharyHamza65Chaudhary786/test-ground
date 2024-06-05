import fnmatch
import os
import sys
import calendar

highest_temp= ['date',-50]                     # highest_temp[0] would contain date and temp[1] would contain max_temp on that day
lowest_temp= ['date',50]
highest_humidity=['date',-50]


# def user_input():

#     year=input()
#     return year




def file_name_matching(year,month_name):                         #send null string in case of ingle argument

     for file_name in os.listdir('.'):

        if month_name=="":
            if fnmatch.fnmatch( file_name, '*'+year+'*'):        # check wether file name matches with pattern given as second argument. '*' means could be anything
                file_parsing_year(file_name)

        elif fnmatch.fnmatch(file_name, '*'+year+'_'+month_name[:3]+'*'):  #[:3] because file name only consist 3 alphabets of month_name
            return file_name




def file_parsing_year(file_name):

    global highest_temp, lowest_temp,highest_humidity             #make variables global

    file_open=open(file_name,"r")
    lines = file_open.readlines()[1:]                             # read file after 1 lines. It will return a list containing each line in filecending with \n
 
    for line in lines:                                             # Iterate through each line
        values = line.strip().split(',')                           # Strip any leading/trailing whitespace (like newlines) and split by comma
       
        if(values[3]!="" and int(values[3])<lowest_temp[1] ):       # values[3]!="" because "empty" cann't be converted to int
                                                            
            lowest_temp[1]=int(values[3])
            lowest_temp[0] =values[0]
        
        if(values[1]!=""  and int(values[1])>highest_temp[1]  ):   # values[1]!="" because "empty" cann't be converted to int
            
           highest_temp[1]=int(values[1])
           highest_temp[0] =values[0]
    
        if(values[7]!="" and int(values[7])>highest_humidity[1]):

            highest_humidity[1]=int(values[7])
            highest_humidity[0] =values[0]
        
    file_open.close()
    


def file_parsing_month(file_name):

    average_values=[0,0,0]                                           # list avg_max_temp. avg_min temp, avg_mean_humidity
    file_open=open(file_name,"r")
    lines = file_open.readlines()[1:] 
    total_lines=1
    for line in lines:                                               # Iterate through each line
        total_lines+=1                                               #to calculate total lines in a file
        values = line.strip().split(',')                             # Strip any leading/trailing whitespace (like newlines) and split by comma
        if(values[1]!=""):
            average_values[0]+=int(values[1])
        if(values[3]!=""):
            average_values[1]+=int(values[3])
        if(values[8]!=""):
            average_values[2]+=int(values[8])

    for i in range (len(average_values)):                            #calculate Average
        average_values[i]=average_values[i]/total_lines

    print_tempratures_month(average_values)     
    file_open.close()




def file_parsing_barchart(file_name):
    
     highest_temp_month=0
     highest_temp_on_lowest_day=0
     lowest_temp_month=50
     lowest_temp_on_highest_day=50
    
     file_open=open(file_name,"r")
     lines = file_open.readlines()[1:] 

     for line in lines:                                                  # Iterate through each line                                             
        values = line.strip().split(',')    
        if(values[1]!=""  and int(values[1])>highest_temp_month  ):      # values[1]!="" because "empty" cann't be converted to int
            
           highest_temp_month=int(values[1])
           lowest_temp_on_highest_day=int(values[3])
                      
        if(values[3]!="" and int(values[3])<lowest_temp_month ):         # values[3]!="" because "empty" cann't be converted to int
                                                                
                lowest_temp_month=int(values[3])
                highest_temp_on_lowest_day=int(values[1])

     print_tempratures_bar(highest_temp_month,lowest_temp_on_highest_day,lowest_temp_month,highest_temp_on_lowest_day)

         


def print_tempratures_bar(highest_temp_month,lowest_temp_on_highest_day,lowest_temp_month,highest_temp_on_lowest_day):  #task 5

    for i in range (lowest_temp_on_highest_day):
         print("\033[1;34m+",end=" ",)

    for i in range (highest_temp_month):
         print("\033[1;31m+",end=" ",)                                                              # ANSI colors               

    print("\033[1;35m",lowest_temp_on_highest_day,"C - ",highest_temp_month,"C")                    #Print lowest - highest temp in magenta color

    print("\n")

    for i in range (lowest_temp_month):
         print("\033[1;34m+",end=" ",)

    for i in range (highest_temp_on_lowest_day):
         print("\033[1;31m+",end=" ",)       
                                                                          
    print("\033[1;35m",lowest_temp_month,"C - ",highest_temp_on_lowest_day,"C")                       #Print lowest - highest temp in magenta color



# def print_tempratures_bar(highest_temp_month,lowest_temp_on_highest_day,lowest_temp_month,highest_temp_on_lowest_day):   # task 3

#     for i in range (highest_temp_month):
#          print("\033[1;31m+",end=" ",)                              # ANSI colors            
#     print("\033[1;35m",highest_temp_month,"C")                      #Print highest temp in magenta color
    
#     print("\n")
#     for i in range (lowest_temp_on_highest_day):
#          print("\033[1;34m+",end=" ",)
#     print("\033[1;35m",lowest_temp_on_highest_day,"C")              #Print highest temp in magenta color

#     print("\n")

#     for i in range (highest_temp_on_lowest_day):
#          print("\033[1;31m+",end=" ",)                              # ANSI colors            
#     print("\033[1;35m",highest_temp_on_lowest_day,"C")              #Print highest temp in magenta color
    
#     print("\n")
#     for i in range (lowest_temp_month):
#          print("\033[1;34m+",end=" ",)
#     print("\033[1;35m",lowest_temp_month,"C")                       #Print highest temp in magenta color




def print_tempratures_year():

    print("highest temp is : ", highest_temp[1], "C on ", highest_temp[0])
    print("lowest temp is : ", lowest_temp[1], "C on ", lowest_temp[0])
    print("highest humidity percentage is : ", highest_humidity[1],"% on ", highest_humidity[0])




def print_tempratures_month(average_values):
    print("highest AVG temp is : ", average_values[0], "C ")
    print("lowest AVG temp is : ", average_values[1],"C ")
    print("highest AVG humidity percentage is : ", average_values[2],"%")




def main():
    cmd_argumentList = sys.argv[1:]                              #stores command line arguments in cmd_ variable. Ignore first bcz it is file name
    for i in  range (len(cmd_argumentList)):

        if cmd_argumentList[i]=='-e':
            print("\n")
            year=cmd_argumentList[i+1]
            
            file_name_matching(year,"")                          #return file_name that matches argument
            print_tempratures_year()
            print("\033[1;32m----------------------------------------------------------------------------------\033[0m",end="")

        if cmd_argumentList[i]=='-a':
            values=cmd_argumentList[i+1].split('/')                # split second argument by ('/') as date-argument would be 2004/6 so values[0] would have year
            year=values[0] 
            month_name=calendar.month_name[int(values[1])]       #convert month number to month name
            file_name=file_name_matching(year,month_name) 
            print("\n\nData for ",year,month_name,"\n")
            file_parsing_month(file_name)
            print("\033[1;32m----------------------------------------------------------------------------------\033[0m",end="")

        if cmd_argumentList[i]=='-c':
            values=cmd_argumentList[i+1].split('/')                # split second argument by ('/') as date-argument would be 2004/6 so values[0] would have year
            year=values[0] 
            month_name=calendar.month_name[int(values[1])]       #convert month number to month name
            file_name=file_name_matching(year,month_name) 
            print("\n\nBar Chart for ",year,month_name,"\n")
            file_parsing_barchart(file_name)
            print("\033[1;32m----------------------------------------------------------------------------------\033[0m",end="")
            print("\n")

            


if __name__ == "__main__":
    main()