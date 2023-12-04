from textSummerizerEnglish.entity import DataTransformationconfig
from textSummerizerEnglish.logging import logger
from transformers import AutoTokenizer
from datasets import load_dataset, Dataset
import pandas as pd
import os


class DataTransformation:
    def __init__(self, config:DataTransformationconfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['ctext'] , max_length = 1024, truncation = True )

        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['text'], max_length = 128, truncation = True )

        return {
            'input_ids' : input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }
    
    def convert(self):
        train_df = pd.read_csv(os.path.join(self.config.data_path, "train", "train.csv"),encoding="latin-1")
        train_df = train_df.dropna()
        train_data = Dataset.from_pandas(train_df)

        test_df = pd.read_csv(os.path.join(self.config.data_path, "test", "test.csv"),encoding="latin-1")
        test_df = test_df.dropna()
        test_data = Dataset.from_pandas(test_df)

        val_df = pd.read_csv(os.path.join(self.config.data_path, "val", "val.csv"),encoding="latin-1")
        val_df = val_df.dropna()
        val_data = Dataset.from_pandas(val_df)


        train_pt = train_data.map(self.convert_examples_to_features, batched = True)
        test_pt = test_data.map(self.convert_examples_to_features, batched = True)
        val_pt = val_data.map(self.convert_examples_to_features, batched = True)

        train_pt.save_to_disk(os.path.join(self.config.root_dir, "new_summary", "train"))
        test_pt.save_to_disk(os.path.join(self.config.root_dir, "new_summary", "test"))
        val_pt.save_to_disk(os.path.join(self.config.root_dir, "new_summary", "val"))