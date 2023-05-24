class Configurable:
    def __init__(self):
        self.section_name = None
        self.config = None
    # load config function
    def load_config(self):
        pass

    # store config
    def store_config(self):
        pass

    def set_config(self, config):
        self.config = config
        return self