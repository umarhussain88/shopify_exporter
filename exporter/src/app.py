from typing import Optional
import logging
import platform
from pathlib import Path
from helpers import (src_dict, 
                    create_file_timestamp, 
                    get_newest_file,
                    output_columns,
                    toast_builder)
import pandas as pd


p = Path(__file__).parent.parent.joinpath('logs')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

if not Path(__file__).parent.parent.joinpath('logs').is_dir():
    Path(__file__).parent.parent.joinpath('logs').mkdir(parents=True)

file_handler = logging.FileHandler(p.joinpath(f'{create_file_timestamp()}_export.log'))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info(f"Starting logging - src_path: {src_dict['src_path']} run by {src_dict['user']}")

if not src_dict['src_path'].is_dir():
    logger.critical("src_path not valid path")
    if platform.system() == 'Windows':
        toast_builder(src_dict['file_not_found'])
        

def transform_raw_data(raw_path : str, extension: Optional[str] = 'xls') -> pd.DataFrame:

    raw_file = get_newest_file(raw_path, extension)

    raw_file_name = raw_file.name.encode('utf-8')
    logger.info(f'parsing {raw_file_name}')

    try:
        raw_df = pd.read_excel(raw_file)
    except FileNotFoundError as e:
        logger.critical(e)(e)
    # remove total column, has chinese character in so will use interger slicing. 
    raw_df = raw_df.iloc[:,:-1]
    # chinese char again so rename using list slicing.
    raw_df = raw_df.rename(columns={raw_df.columns[0] : 'src_sku'})
    raw_transform = pd.melt(raw_df,
                            id_vars='src_sku',
                            var_name='Option1 Value', 
                            value_name='70 rue de la prulay').dropna(subset=['70 rue de la prulay']
                            )
    raw_transform['SKU'] = ( raw_transform['src_sku'].str.replace('\(.*\)','',regex=True) 
                            + '-' 
                            + raw_transform['Option1 Value']).str.strip()
    raw_transform['SKU'] = raw_transform['SKU'].str.replace('-F', '',regex=False)

    logger.info(f"shape of raw_transform dataframe {raw_transform.shape}")

    return raw_transform


def dimension_lookups(dimension_path : str, extension : Optional[str] = 'xlsx') -> pd.DataFrame:

    dim_path = get_newest_file(dimension_path,extension)

    logger.info(f'reading dimension dataframe: {dim_path}')

    try:
        dim_df = pd.read_excel(dim_path,engine='openpyxl')
    except FileNotFoundError as e:
        logger.critical(e)

    return dim_df



def create_shopify_export(raw_df : pd.DataFrame, 
                         dim_df : pd.DataFrame,
                         output_columns : list,
                         output_path : str,
                         file_timestamp : str
                         ) -> pd.DataFrame:

    result = pd.merge(raw_df.drop('Option1 Value',axis=1),
                    dim_df,
                    on=['SKU'],
                    how='left')

    #assign missing columns
    result = result.assign(**{col : pd.NA for col in output_columns if not col in result.columns})
    result_final = result[output_columns]
    result_final = result_final.sort_values(['SKU'])

    out_path = output_path.joinpath(f"{file_timestamp}_result.csv")

    result_final.dropna(subset=['Handle']).to_csv(out_path, index=False)

    logger.info(f"file exported to {out_path}")

    return result_final[result_final['Handle'].isna()==True]


def create_missing_output(missing_df : pd.DataFrame) -> None:
    #TODO
    #create sku/handle like output
    #fill in missing handles using SOURCE sku.
    #output to file.
    #maybe create an audit file to show how many missing skus there are W2W and if the missing sku exisited in prior weeks. 
    pass


def main():
    try:
        dt = create_file_timestamp() 
        raw_df = transform_raw_data(src_dict['raw'], 'xls')
        dim_df = dimension_lookups(src_dict['dim'])
        missing_df = create_shopify_export(raw_df, dim_df, output_columns, src_dict['output'], dt)
        create_missing_output(missing_df)
        toast_builder(src_dict['sucess_toast'])
    except Exception as e:
         
        logger.info(e)
        






if __name__ == '__main__':
    main()