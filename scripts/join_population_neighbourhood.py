import pandas as pd
import glob
import re

csv_files = glob.glob('../data/madrid/raw/population/population_total_D*.csv')


all_neight = pd.DataFrame()
for file in csv_files:
    data = pd.read_csv(file)
    total = data[data.columns[data.columns.str.contains('total')]].reset_index(drop=True)
    total.columns = [col.replace('_total','').strip() for col in total.columns.values]
    pattern = re.compile("\d{2}._")
    columns_to_drop = [col for col in total.columns if pattern.match(col)]
    total = total.drop(columns=columns_to_drop)
    total.columns = ['_'.join(col.split('_')[1:]).title() for col in total.columns]
    total.columns = [col.rstrip('_') for col in total.columns]
    
    total_values = pd.DataFrame(total.sum())
    total_values['neigbourhood'] = total_values.index
    total_values.reset_index(drop=True,inplace=True)
    total_values.rename(columns={0:'total'}, inplace=True)
    total_values = total_values.reindex(columns=['neigbourhood','total'])
    total_values['total'] = total_values['total'].astype(int)
    total_values['neigbourhood'] = total_values['neigbourhood'].str.replace('_',' ')
    total_values.to_csv(f'../data/madrid/raw/population/total/{file.split("/")[-1]}', index=False)
    all_neight = pd.concat([all_neight, total_values], axis=0)

all_neight.to_csv('../data/madrid/cleaned/total_by_neighbourhood.csv', index=False)