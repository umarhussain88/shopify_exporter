from pathlib import Path
from environs import Env
import getpass

TEST = False 
src_dict = {}

if TEST:
       e = Env()
       e.read_env('../.env')
       src_path = Path(e('src_path'))
else:
       import pandas as pd
       # could just open as json, but this works for now.
       p = pd.read_json(Path(__file__).parent.parent.parent.joinpath('config.json'))['src_path'].tolist()[0]
       src_path = Path(p)
       

src_dict['src_path']    = src_path
src_dict['raw']         = src_path.joinpath('raw_data')
src_dict['dim']         = src_path.joinpath('dimension_lookups')
src_dict['output']      = src_path.joinpath('output') 
src_dict['missing_sku'] = src_path.joinpath('missing_sku') 
src_dict['user']        = getpass.getuser()

output_columns = ['Handle', 'SKU', 'Option1 Name', 'Option1 Value', 'Option2 Name',
       'Option2 Value', 'Option3 Name', 'Option3 Value',
       '70 rue de la prulay']