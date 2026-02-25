import os
import shutil
import random
from pathlib import Path

def create_sampled_dataset(source_root, target_root, train_samples=5000, test_samples=100, valid_samples=100):
    """
    Sample random image pairs (CD30/HES) from source dataset and create new dataset structure.
    
    Args:
        source_root: Path to source dataset
        target_root: Path to target dataset
        train_samples: Number of samples to take from train set
        test_samples: Number of samples to take from test set
        valid_samples: Number of samples to take from valid set
    """
    source_root = Path(source_root)
    target_root = Path(target_root)
    
    # Create target directory structure
    target_root.mkdir(parents=True, exist_ok=True)
    
    splits = {
        'train': train_samples,
        'test': test_samples,
        'valid': valid_samples
    }
    
    for split, num_samples in splits.items():
        source_split = source_root / split
        
        # Get all CD30 files
        cd30_files = sorted([f for f in (source_split / 'CD30').glob('*') if f.is_file()])
        
        # Randomly sample
        sampled_files = random.sample(cd30_files, min(num_samples, len(cd30_files)))
        
        # Create target directories
        target_cd30 = target_root / split / 'CD30'
        target_hes = target_root / split / 'HES'
        target_cd30.mkdir(parents=True, exist_ok=True)
        target_hes.mkdir(parents=True, exist_ok=True)
        
        # Copy paired files
        for cd30_file in sampled_files:
            hes_file = source_split / 'HES' / cd30_file.name
            
            if hes_file.exists():
                shutil.copy2(cd30_file, target_cd30 / cd30_file.name)
                shutil.copy2(hes_file, target_hes / hes_file.name)
                print(f"Copied: {cd30_file.name}")
        
        print(f"{split}: {len(sampled_files)} pairs copied\n")

if __name__ == "__main__":
    source = "/home/naiken/coding/cDDPM/dataset"
    target = "/home/naiken/coding/cDDPMv2/dataset"
    
    create_sampled_dataset(source, target)
    print("Dataset creation completed!")