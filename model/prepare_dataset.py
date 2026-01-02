"""
Utility script to prepare dataset for YOLO training
"""
import os
import shutil
from pathlib import Path
import yaml


def prepare_dataset_structure(base_path: str = "dataset"):
    """
    Create YOLO dataset directory structure
    
    Args:
        base_path: Base directory for dataset
    """
    # Create directory structure
    dirs = [
        f"{base_path}/images/train",
        f"{base_path}/images/val",
        f"{base_path}/images/test",
        f"{base_path}/labels/train",
        f"{base_path}/labels/val",
        f"{base_path}/labels/test",
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created: {dir_path}")
    
    print("\nDataset structure created!")
    print("Next steps:")
    print("1. Add your training images to dataset/images/train/")
    print("2. Add corresponding label files (.txt) to dataset/labels/train/")
    print("3. Add validation images to dataset/images/val/")
    print("4. Add validation labels to dataset/labels/val/")
    print("5. Update data.yaml with your class names")


def create_data_yaml(
    output_path: str = "data.yaml",
    dataset_path: str = "./dataset",
    classes: list = None
):
    """
    Create data.yaml configuration file
    
    Args:
        output_path: Output path for data.yaml
        dataset_path: Path to dataset directory
        classes: List of class names
    """
    if classes is None:
        classes = [
            "Coca Cola",
            "Pepsi",
            "Water Bottle",
            "Chips",
            "Snacks",
            "Energy Drink"
        ]
    
    config = {
        "path": dataset_path,
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": len(classes),
        "names": {i: name for i, name in enumerate(classes)}
    }
    
    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"Created data.yaml at {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare YOLO dataset structure")
    parser.add_argument("--base-path", type=str, default="dataset", help="Base dataset path")
    parser.add_argument("--create-yaml", action="store_true", help="Create data.yaml file")
    
    args = parser.parse_args()
    
    prepare_dataset_structure(args.base_path)
    
    if args.create_yaml:
        create_data_yaml()




