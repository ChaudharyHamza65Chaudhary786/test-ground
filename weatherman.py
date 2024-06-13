import argparse
import Driver


def main():

    """
    It initializes a Driver instance to handle commands and uses the argparse module to parse command-line arguments.
    The script provides the following options:

    """

    cmd_handler = Driver.Driver()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help="To print Report for year")
    parser.add_argument('-a', help="To print AVG Report ")
    parser.add_argument('-c', help="To print Barchart Report")
    args = parser.parse_args()
    cmd_handler.handle_cmd_arguments(args)


if __name__ == "__main__":
    main()
