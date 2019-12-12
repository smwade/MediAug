import os
from os.path import join
from pathlib import Path
import urllib.request
import zipfile


def download_sipakmed(data_dest=None):
    """ Download the SIPaKMeD dataset, http://cs.uoi.gr/~marina
    Args:
      data_dest (str): The path of dir to store data. If noe will default to package cache
    Returns:
      None
    """
    if data_dest is None:
        data_dest = join(get_data_cache(), 'sipakmed_raw')
    if os.path.exists(data_dest):
        raise ValueError('Data already downloaded.')
    os.mkdir(data_dest)

    file_urls = [
        'http://cs.uoi.gr/~marina/SIPAKMED/im_Metaplastic.7z',
        'http://cs.uoi.gr/~marina/SIPAKMED/im_Dyskeratotic.7z'
        'http://cs.uoi.gr/~marina/SIPAKMED/im_Koilocytotic.7z',
        'http://cs.uoi.gr/~marina/SIPAKMED/im_Parabasal.7z',
        'http://cs.uoi.gr/~marina/SIPAKMED/im_Superficial-Intermediate.7z',
    ]
    cell_types = [
        'metaplastic',
        'dyskeratotic',
        'koilocytotic'
        'parabasal',
        'superficial-Intermediate',
    ]

    print(f'Downloading SIPaKMed to: {data_dest}')
    for url, cell_type in zip(file_urls, cell_types):
        print(f'Downloading {cell_type}...')
        file_name = f'{cell_type}.zip'
        urllib.request.urlretrieve(url, join(data_dest, file_name))

    for file_name in data_dest:
        print(f'Extracting {file_name}...')
        with zipfile.ZipFile(file_urls) as f:
            f.extract(file_name, dir)
        os.remove(file_name)

    print('Finished downloading.')
    

def download_smear(data_dest=None):
    """ Download the Hervel smear dataset
    Args:
      data_dest (str): The path of dir to store data. If noe will default to package cache
    Returns:
      None
    """
    raise NotImplementedError('Get it yourself, not implemented.')


def get_data_cache():
    """ Get the cache where datasets are stored. Defaults to ~/.mediaug
    Args:
      None
    Returns:
      path (str): The path to the data cache on the system
    """
    p = Path(join(Path.home(), '.mediaug'))
    p.mkdir(exist_ok=True)
    return str(p)
