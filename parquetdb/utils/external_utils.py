import os
import re
import multiprocessing
from functools import partial
import shutil
import requests
import bz2
from bs4 import BeautifulSoup

from parquetdb import config

# Function to download the file
def download_file(file_url, output_path):
    """
    Downloads a file from the specified URL to a local output path.

    Parameters
    ----------
    file_url : str
        The URL of the file to download.
    output_path : str
        The local file path where the downloaded file will be saved.

    Example
    -------
    >>> download_file('https://example.com/file.zip', 'data/file.zip')
    Downloaded: data/file.zip
    """
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {output_path}")
    else:
        print(f"Failed to download: {file_url}")
        
        
def download_file_mp_task(file_name, url = "https://alexandria.icams.rub.de/data/pbe/", output_dir='.'):
    """
    Downloads a file by combining the base URL and file name, then saves it to the specified output directory.

    Parameters
    ----------
    file_name : str
        The name of the file to download.
    url : str, optional
        The base URL to use for downloading files. Default is 'https://alexandria.icams.rub.de/data/pbe/'.
    output_dir : str, optional
        The directory where the downloaded file will be saved. Default is the current directory.

    Example
    -------
    >>> download_file_mp_task('alexandria_data.json.bz2', output_dir='data/downloads')
    Downloaded: data/downloads/alexandria_data.json.bz2
    """
    file_url = url + file_name
    output_path = os.path.join(output_dir, file_name)
    download_file(file_url, output_path)

# Scrape the page to find all file links that match the pattern
def scrape_files(output_dir='data/external/alexandria/uncompressed', n_cores=1):
    """
    Scrapes a web page to find all file links matching the pattern `alexandria_***.json.bz2` and downloads them.

    Parameters
    ----------
    output_dir : str, optional
        The directory where the downloaded files will be saved. Default is 'data/external/alexandria/uncompressed'.
    n_cores : int, optional
        The number of CPU cores to use for downloading files in parallel. Default is 1 (no multiprocessing).

    Example
    -------
    >>> scrape_files(output_dir='data/downloads', n_cores=4)
    Using Multiprocessing
    """
    
    os.makedirs(output_dir, exist_ok=True)
    # The URL of the page to scrape
    url = "https://alexandria.icams.rub.de/data/pbe/"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links that match the pattern alexandria_***.json.bz2
    file_links = []
    for link in soup.find_all('a', href=True):
        file_name = link['href']
        if re.match(r'alexandria_.*\.json\.bz2', file_name):
            file_links.append(file_name)

    if not file_links:
        print("No files found matching the pattern.")
        return

    # Download each file
    if n_cores!=1:
        print("Using Multiprocessing")
        with multiprocessing.Pool(processes=n_cores) as pool:
            results=pool.map(partial(download_file_mp_task, url=url, output_dir=output_dir), file_links)
    else:
        print("Not Using Multiprocessing")
        for file_link in file_links:
            download_file(file_link, url, output_dir)
        

def decompress_bz2_file(file_name, source_dir='compressed', dest_dir='uncompressed'):
    """
    Decompresses a .bz2 file and saves the decompressed content to the destination directory.

    Parameters
    ----------
    file_name : str
        The name of the .bz2 file to decompress.
    source_dir : str, optional
        The directory containing the .bz2 file. Default is 'compressed'.
    dest_dir : str, optional
        The directory where the decompressed file will be saved. Default is 'uncompressed'.

    Example
    -------
    >>> decompress_bz2_file('data.bz2', source_dir='compressed', dest_dir='uncompressed')
    Decompressed: compressed/data.bz2 -> uncompressed/data
    """
    if file_name.endswith('.bz2'):
        # Path to the .bz2 file
        bz2_file_path = os.path.join(source_dir, file_name)

        # Decompressed file path (remove the .bz2 extension)
        decompressed_file_name = file_name[:-4]
        decompressed_file_path = os.path.join(dest_dir, decompressed_file_name)

        # Decompress the file
        with bz2.BZ2File(bz2_file_path, 'rb') as file_in:
            with open(decompressed_file_path, 'wb') as file_out:
                file_out.write(file_in.read())
        
        print(f"Decompressed: {bz2_file_path} -> {decompressed_file_path}")
        
def decompress_bz2_files(source_dir, dest_dir, n_cores):
    """
    Decompresses all .bz2 files in the source directory using multiple cores.

    Parameters
    ----------
    source_dir : str
        The directory containing the .bz2 files.
    dest_dir : str
        The directory where decompressed files will be saved.
    n_cores : int
        The number of CPU cores to use for parallel decompression.

    Example
    -------
    >>> decompress_bz2_files('compressed', 'uncompressed', n_cores=4)
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Loop through all files in the source directory
    filenames=os.listdir(source_dir)
    
    if n_cores!=1:
        with multiprocessing.Pool(n_cores) as pool:
            results = pool.map(partial(decompress_bz2_file, source_dir=source_dir, dest_dir=dest_dir), filenames)
    else:
        for filename in filenames:
            decompress_bz2_file(filename, source_dir, dest_dir)

def download_alexandria_3d_database(output_dir, n_cores=8, from_scratch=False):
    """
    Downloads and decompresses the Alexandria 3D database.

    Parameters
    ----------
    output_dir : str
        The directory where the database will be downloaded and stored.
    n_cores : int, optional
        The number of CPU cores to use for downloading and decompressing files. Default is 8.
    from_scratch : bool, optional
        If True, removes any existing data and starts the download process from scratch. Default is False.

    Returns
    -------
    str
        The path to the destination directory containing the decompressed database.

    Example
    -------
    >>> destination_dir = download_alexandria_3d_database(output_dir='data/alexandria', n_cores=4, from_scratch=True)
    """
    # Create a folder to save the downloaded files
    if from_scratch and os.path.exists(output_dir):
        print(f"Removing existing directory: {output_dir}")
        shutil.rmtree(output_dir, ignore_errors=True)
        
    os.makedirs(output_dir, exist_ok=True)
    source_directory = os.path.join(output_dir, 'compressed')
    destination_directory = os.path.join(output_dir, 'uncompressed')
    
    os.makedirs(destination_directory, exist_ok=True)
    os.makedirs(source_directory, exist_ok=True)
    
    if len(os.listdir(destination_directory))>0:
        print("Database downloaded already. Skipping download.")
        return destination_directory
    
    
    scrape_files(output_dir=source_directory, n_cores=n_cores)
    decompress_bz2_files(source_directory, destination_directory,n_cores=n_cores)
    
    return destination_directory