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

        self.parser.add_argument('--show', dest='show_plot', 
                                 action='store_const', const=True, default=False,
                                 help='Show plots during program run')

        self.parser.add_argument('-d', metavar='DISEASE', dest='disease', 
                                 type=str, default='Measles',
                                 choices=['Hepatitis A', 'Measles', 'Mumps',
                                          'Pertussis', 'Polio', 'Rubella', 'Smallpox'],
                                 help='Specify disease to work with: Hepatitis A, '
                                      'Measles, Mumps, Pertussis, Polio, '
                                      'Rubella or Smallpox (default Measles)')

        self.parser.add_argument('-s', metavar='STATE', dest='states', 
                                 type=str, nargs='+', default=['California'],
                                 choices=['Alabama', 'Alaska', 'Arizona', 'Arkansas',
                                          'California', 'Colorado', 'Connecticut',
                                          'Delaware','District Of Columbia', 'Florida',
                                          'Georgia', 'Hawaii', 'Idaho', 'Illinois',
                                          'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                                          'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
                                          'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                                          'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                                          'New Jersey', 'New Mexico', 'New York',
                                          'North Carolina', 'North Dakota', 'Ohio',
                                          'Oklahoma', 'Oregon', 'Pennsylvania',
                                          'Rhode Island', 'South Carolina', 'South Dakota',
                                          'Tennessee', 'Texas', 'Utah', 'Vermont',
                                          'Virginia', 'Washington', 'West Virginia',
                                          'Wisconsin', 'Wyoming'],
                                 help='Specify states to work with '
                                      '(default California)')

        self.parser.add_argument('-y', metavar='DECADE', dest='decades', 
                                 type=int, nargs='+', default=[1950, 1960, 1970],
                                 choices=[1930, 1940, 1950, 1960, 1970, 1980],
                                 help='Specify decades to work with: 1930, '
                                      '1940, 1950, 1960, 1970, 1980 '
                                      '(default 1950, 1960 & 1970)')

        self.args = self.parser.parse_args()

    def get_arguments(self):
        return self.args
