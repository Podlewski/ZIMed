import argparse


class ArgumentParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='ZIMed - Task 2',
            formatter_class=argparse.RawTextHelpFormatter,
            description='Lodz University of Technology (TUL)'
                        '\nComputer Applications in Medicine'
                        ' (Zastosowania informatyki w medycynie)'
                        '\n\nTask2'
                        '\n\nAuthors:'
                        '\n  Paweł Jeziorski\t234066'
                        '\n  Barbara Morawska\t234096'
                        '\n  Karol Podlewski\t234106'
                        '\n  Andrzej Sasinowski\t234118')

        self.parser.add_argument('--time', dest='time', action='store_const',
                                 const=True, default=False,
                                 help='Print time measurement (might not work \
                                       correct with --plot')       

        self.parser.add_argument('--plot', dest='plot', action='store_const',
                                 const=True, default=False,
                                 help='Show plots')                                  

        self.args = self.parser.parse_args()

    def get_arguments(self):
        return self.args
