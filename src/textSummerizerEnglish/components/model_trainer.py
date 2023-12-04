from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, DataCollatorForSeq2Seq
from transformers import TrainingArguments, Trainer, pipeline
from textSummerizerEnglish.config.configuration import ModelTrainerConfig
from datasets import load_dataset, Dataset, load_from_disk
from pathlib import Path
import torch
import os

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        
    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_flan = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_flan)

        train_dataset = load_from_disk(Path(os.path.join(self.config.data_path, "new_summary", "train")))
        val_dataset = load_from_disk(Path(os.path.join(self.config.data_path, "new_summary", "val")))

        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir, 
            num_train_epochs=self.config.num_train_epochs,
            warmup_steps=self.config.warmup_steps,
            per_device_eval_batch_size=self.config.per_device_eval_batch_size,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            weight_decay=self.config.weight_decay,
            logging_steps=self.config.logging_steps,
            save_steps=1e6,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            push_to_hub=self.config.push_to_hub,
            report_to=[]
        )

        trainer = Trainer(model=model_flan, 
                          args=trainer_args,
                          tokenizer=tokenizer, 
                          data_collator=seq2seq_data_collator,
                          train_dataset=train_dataset, 
                          eval_dataset=val_dataset)
        trainer.train()

        model_flan.save_pretrained(Path(os.path.join(self.config.root_dir,"Flan-T5-model")))
        ## Save tokenizer
        tokenizer.save_pretrained(Path(os.path.join(self.config.root_dir,"tokenizer")))