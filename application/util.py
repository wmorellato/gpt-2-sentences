import os
import gdown
import requests
from tqdm import tqdm
from gdown import extractall
from urllib.parse import urlparse

def download_file_with_progress(url, output_dir):
    """
        Utility borrowed from gpt-2-simple.
    """
    CHUNK_SIZE = 1024 * 1024

    if 'drive.google.com' in url:
        cwd = os.getcwd()
        os.chdir(output_dir)

        downloaded_file = gdown.download(url)
        os.chdir(cwd)
        
        return extractall(os.path.join(output_dir, downloaded_file))

    filename = os.path.basename(urlparse(url).path)
    r = requests.get(url, stream=True)

    with open(os.path.join(output_dir, filename), 'wb') as f:
        with tqdm(ncols=100, desc='Downloading file from ' + url) as pbar:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
                pbar.update(CHUNK_SIZE)
    
    return extractall(os.path.join(output_dir, filename))