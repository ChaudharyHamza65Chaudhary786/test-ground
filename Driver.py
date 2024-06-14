import calendar
import ReportGenerator
import WeatherFIleHandler


class Driver:

    """ A class to handle command line arguments and generate report against them"""

    report_generator = ReportGenerator.ReportGenerator()
    weather_file_handler = WeatherFIleHandler.WeatherFilesHandler()

    def validate_year_month(self, year, month_num): 

        """
        Input validation for year and month

        
        Args:
            year : year for which all files should be read
            month_num : month number for file
        
        Return: 
            True if all conditions are satisfie else False

        """

        try:
            calendar.month_abbr[int(month_num)]
            flag = True
        except:
            print("INVALID Year or Month Entered")
            flag = False

        return year.isnumeric() and month_num.isnumeric() and flag
    
    def parse_year_and_month_from_arguments(self, cmd_argument):
        
        """
        parse year and month from command line arguments
        
        Args:
            cmd_argument : argument string that contains year and month
        
        Return: 
            parsed_date_info : year in arguments[0] and month number n arguments[1]

        """
        arguments = cmd_argument.split('/')            
        return arguments[0], arguments[1]
    
    def process_arguments_and_give_file_name(self, cmd_args):
        """
        Processes the date_arguments provided and retrieves the corresponding weather file name.
       
        Args:
            args : Contains date
        
        Returns:
            The filename corresponding to the provided year and month, if valid. Otherwise, returns None.
        """
        file_name = None
        year, month = self.parse_year_and_month_from_arguments(cmd_args)
        if self.validate_year_month(year, month): 
            month = calendar.month_abbr[int(month)]       
            file_name = self.weather_file_handler.match_and_extract_file_name(year, month)      
            
        return file_name
        
    
    def handle_cmd_arguments(self, cmd_args):

        """
        Handles command-line arguments and performs corresponding actions based on the provided options.
       
        Args:
            cmd_args (Namespace): An object containing parsed command-line arguments.
        
        Actions:
        - If the '-e' flag is provided, generates a report for all files of specified year.
        - If the '-a' flag is provided, generates a report for the specified month and year.
        - If the '-c' flag is provided, generates a bar chart for the specified month and year.

        """
       
        if cmd_args.e: 
            files_name = self.weather_file_handler.match_and_extract_file_name(cmd_args.e)
            if files_name:
                self.report_generator.generate_report_for_year_handler(files_name)
            else:
                print(f"No Record Found for year {cmd_args.e}")
        
        if cmd_args.a:
                file_name = self.process_arguments_and_give_file_name(cmd_args.a)
                if file_name:
                    self.report_generator.generate_average_report_handler(file_name)         
            
        if cmd_args.c:
                file_name = self.process_arguments_and_give_file_name(cmd_args.c)
                if file_name:
                    self.report_generator.generate_barchart_for_file_handler(file_name)

