'''Loads Configuration from an ini file'''

from configparser import ConfigParser


class EvalExConfig(ConfigParser):
    '''
    Implement configuration options for evaluation of the Exomizer.
    '''

    def __init__(
            self,
            conf_file: str = "config.ini"
    ):
        self.path = conf_file
        super().__init__()
        self.read(self.path)
