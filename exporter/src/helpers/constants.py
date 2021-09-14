from pathlib import Path
import getpass
from pathlib import Path 


TEST = False 
src_dict = {}

if TEST:
       from environs import Env
       e = Env()
       e.read_env('../.env')
       src_path = Path(e('src_path'))
else:
       import pandas as pd
       # could just open as json, but this works for now.
       df = pd.read_excel(Path(__file__).parent.parent.parent.joinpath('config.xlsx'))
       p = df[df['config_name'].eq('source_path')]['config_value'].tolist()[0]
       src_path = Path(fr"{p}")
       

src_dict['src_path']    = src_path
src_dict['raw']         = src_path.joinpath('raw_data')
src_dict['dim']         = src_path.joinpath('dimension_lookups')
src_dict['output']      = src_path.joinpath('output') 
src_dict['missing_sku'] = src_path.joinpath('missing_sku') 
src_dict['user']        = getpass.getuser()

output_columns = ['Handle', 'SKU', 'Option1 Name', 'Option1 Value', 'Option2 Name',
       'Option2 Value', 'Option3 Name', 'Option3 Value',
       '70 rue de la prulay']



### TOAST MESSAGES

#file not found.

src_dict['file_not_found'] = f"""
        <toast>
            <visual>
            <binding template='ToastGeneric'>
                <text>Shopify Export, File Not Found Error!</text>
                <text>Hi {getpass.getuser()} - {src_path}\n is not a valid path - for help, please refer to the instructions.</text>
            </binding>
            </visual>
            <actions>
            <action
                content="Dismiss"
                arguments="action=dismiss"/>
            </actions>        
        </toast>
        """

src_dict['sucess_toast'] = f"""
                            <toast>
                            <visual>
                            <binding template='ToastGeneric'>
                                   <text>Shopify Export Complete!</text>
                                   <text>Hi {getpass.getuser()} - your file has finished processing, check the output folder.</text>
                            </binding>
                            </visual>
                            <actions>
                            <action
                                   content="Dismiss"
                                   arguments="action=dismiss"/>
                            </actions>        
                            </toast>
                            """     
