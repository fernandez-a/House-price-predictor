import pandas as pd
import glob

csv_files = glob.glob('../data/madrid/raw/population/population_total_D*.csv')


all_neight = pd.DataFrame()
for file in csv_files:
    data = pd.read_csv(file)
    total = data[data.columns[data.columns.str.contains('total')]].reset_index(drop=True)
    total.columns = [col.replace('total','') for col in total.columns.values]
    total.columns = ['_'.join(col.split('_')[1:]) for col in total.columns.values]
    total.columns = [col.rstrip('_') for col in total.columns]
    
    total_values = pd.DataFrame(total.sum())
    total_values['district'] = total_values.index
    total_values.reset_index(drop=True,inplace=True)
    total_values.rename(columns={0:'total'}, inplace=True)
    total_values = total_values.reindex(columns=['district','total'])
    total_values['total'] = total_values['total'].astype(int)
    total_values['district'] = total_values.district.str.title()
    total_values['district'] = total_values['district'].str.replace('_',' ')
    total_values.to_csv(f'../data/madrid/raw/population/total/{file.split("/")[-1]}', index=False)
    all_neight = pd.concat([all_neight, total_values], axis=0)

all_neight.to_csv('../data/madrid/cleaned/total_by_neighbourhood.csv', index=False)