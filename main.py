import shutil
import os
from tqdm import tqdm

def copy_file_with_progress(src, dst_folder, buffer_size=1024*1024):
    """
    Copy a file from src to a destination folder with a progress bar.
    
    :param src: Source file path.
    :param dst_folder: Destination folder path.
    :param buffer_size: Buffer size for reading the file in chunks. Default is 1MB.
    """
    if not os.path.isdir(dst_folder):
        raise ValueError("Destination must be a directory.")
    
    # Get the file name from the source path
    file_name = os.path.basename(src)
    # Create the full destination path
    dst = os.path.join(dst_folder, file_name)
    
    total_size = os.path.getsize(src)
    copied_size = 0
    
    with open(src, 'rb') as src_file, open(dst, 'wb') as dst_file:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name) as pbar:
            while True:
                buffer = src_file.read(buffer_size)
                if not buffer:
                    break
                dst_file.write(buffer)
                copied_size += len(buffer)
                pbar.update(len(buffer))

def copy_directory_with_progress(src, dst):
    """
    Recursively copy a directory from src to dst with a progress bar.
    
    :param src: Source directory path.
    :param dst: Destination directory path.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(src):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    copied_size = 0
    
    with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(src)) as pbar:
        for dirpath, dirnames, filenames in os.walk(src):
            for dirname in dirnames:
                src_dir = os.path.join(dirpath, dirname)
                dst_dir = os.path.join(dst, os.path.relpath(src_dir, src))
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
            for filename in filenames:
                src_file = os.path.join(dirpath, filename)
                dst_file = os.path.join(dst, os.path.relpath(src_file, src))
                with open(src_file, 'rb') as sf, open(dst_file, 'wb') as df:
                    while True:
                        buffer = sf.read(1024*1024)
                        if not buffer:
                            break
                        df.write(buffer)
                        copied_size += len(buffer)
                        pbar.update(len(buffer))

def copy_with_progress(src, dst_folder):
    """
    Copy a file or directory from src to a destination folder with a progress bar.
    
    :param src: Source file or directory path.
    :param dst_folder: Destination folder path.
    """
    if os.path.isfile(src):
        copy_file_with_progress(src, dst_folder)
    elif os.path.isdir(src):
        dst_dir = os.path.join(dst_folder, os.path.basename(src))
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        copy_directory_with_progress(src, dst_dir)
    else:
        raise ValueError("Source must be a file or directory.")


if __name__ == "__main__":
    src_path = "path/to/source" # 替換為源檔案的路徑
    dst_path = "path/to/destination/folder"  # 替換為目標檔案的路徑
    copy_with_progress(src_path, dst_path)
