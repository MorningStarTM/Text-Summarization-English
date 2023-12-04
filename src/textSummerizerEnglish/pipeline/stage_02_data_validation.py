from textSummerizerEnglish.config.configuration import ConfigurationManager
from textSummerizerEnglish.components.data_validation import DataValidation

from textSummerizerEnglish.logging import logger

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        #print(data_validation_config)
        data_validation = DataValidation(config=data_validation_config)
        data_validation.valid_all_file_exist()