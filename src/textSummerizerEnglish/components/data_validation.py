import os
import zipfile
from textSummerizerEnglish.logging import logger
from textSummerizerEnglish.utils.common import get_size
from pathlib import Path
from textSummerizerEnglish.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config=DataValidationConfig):
        self.config = config

    
    def valid_all_file_exist(self) -> bool:
        try:
            validation_status = None
            all_files = os.listdir(os.path.join("artifacts", "data_ingestion"))

            for file in all_files:
                if file not in self.config.ALL_REQUIRED_FILES:
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"validation status: {validation_status}")

                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"validation status: {validation_status}")
                        
            return validation_status

        
        except Exception as e:
            logger.exception(e)
            raise e