from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_fir: Path
    STATUS_FILE: str
    ALL_REQUIRED_FILES: list


@dataclass(frozen=True)
class DataTransformationconfig:
    root_dir: Path
    data_path: Path
    tokenizer_name: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    model_ckpt: Path
    num_train_epochs: int
    warmup_steps: int
    per_device_train_batch_size: int
    per_device_eval_batch_size: int
    weight_decay: float
    save_steps: str
    gradient_accumulation_steps: int
    logging_steps: int
    push_to_hub: bool
    report_to: list

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    data_path: Path
    model_path: Path
    tokenizer_path: Path
    metric_file_name: Path