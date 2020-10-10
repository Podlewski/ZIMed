import argparse


class ArgumentParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='ZIMed - Task 1',
            formatter_class=argparse.RawTextHelpFormatter,
            description='Lodz University of Technology (TUL)'
                        '\nComputer Applications in Medicine'
                        ' (Zastosowania informatyki w medycynie)'
                        '\n\nTask1'
                        '\n\nAuthors:'
                        '\n  Paweł Jeziorski\t???'
                        '\n  Barbara Morawska\t???'
                        '\n  Karol Podlewski\t234106'
                        '\n  Andrzej Sasinowski\t???') 

        self.parser.add_argument('-s', '--show', dest='show_plot', 
                                 action='store_const', const=True, default=False,
                                 help='Show plots during program run')

        self.args = self.parser.parse_args()


    def get_arguments(self):
        return self.args
