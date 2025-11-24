import pyvista as pv
import numpy as np
import pandas as pd
import os
import re
from sklearn.preprocessing import MinMaxScaler
from pyqreg import QuantReg
from patsy import dmatrices
from scipy.stats import norm
from copy import deepcopy
import argparse

# Parse command-line arguments ############################################################
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, required=True, help="Path to the input folder")
parser.add_argument("--output_dir", type=str, required=True, help="Path to the output folder")
parser.add_argument("--tau_all", type=str, default="0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95",
                    help="Comma-separated list of quantiles (e.g., 0.05,0.1,0.2)")

args = parser.parse_args()

# Define Directories ############################################################
Data_Path = os.path.join(args.input_dir, "FiberTracts/")
Doc_Path = args.input_dir
Output_Path = args.output_dir
os.makedirs(Output_Path, exist_ok=True)

# Parse tau_all string into a numpy array ############################################################
tau_all = np.array([float(t) for t in args.tau_all.split(",")])
NNN = 2000

# Obtain a list of files ############################################################
vtp_files = os.listdir(Data_Path)
N_files = len(vtp_files)



### Deriving Files #############################################################
all_dfs = []  # list to hold all DataFrames
for i in (range(N_files)):
  FileName=vtp_files[i]
  mesh = pv.read(Data_Path+FileName)
  Ncells=mesh.n_cells
  import random
  #NNN = int(len(range(Ncells)) * pct)
  if Ncells>NNN:
    random.seed(1126)
    chosen_integers = random.sample(range(Ncells), NNN)
  else:
    random.seed(1126)
    chosen_integers = random.choices(range(Ncells),k=NNN)
  ID=np.array([])
  for iii in chosen_integers:
    cell = mesh.get_cell(iii)
    ID=np.concatenate((ID,np.array(cell.point_ids)))
  ID=ID.astype(int)
  arr = mesh.point_data['FA1']
  temp = pd.DataFrame(arr[ID], columns=['FA'])
  match = re.search(r'\d+', FileName)
  if match:
    number = int(match.group())
  temp['ID'] = number
  all_dfs.append(temp)  # add the DataFrame to the list
################################################################################


#### Data Linkage ##############################################################
final_df = pd.concat(all_dfs, ignore_index=True)
del all_dfs
Demo = pd.read_csv(Doc_Path+'/Covariate.csv')
data = pd.merge(final_df, Demo, on='ID', how='left')
cols = [col for col in data.columns if col not in ['FA', 'ID']]
print(cols)


Response="FA"
Group="ID"
Fixed = Response + " ~ " + " + ".join(cols)
Y, X = dmatrices(Fixed, data=data, return_type='dataframe')
Pnames=X.columns.tolist()
Y=Y.values.flatten()
X=X.values
GGG = data[Group].values


results = []
for tau in tau_all:
  mod_cluster = QuantReg(Y, X)
  res_cluster= mod_cluster.fit(tau, cov_type='cluster', cov_kwds={'groups': GGG})
  df_cluster = pd.DataFrame({'tau':tau,'predictors':Pnames,'coefficients': res_cluster.params,'SEs': res_cluster.bse,'pvalues': norm.sf(abs(res_cluster.params/res_cluster.bse)) * 2})
  results.append(df_cluster)

OOO = pd.concat(results, ignore_index=True)
OOO.to_csv(Output_Path+'/FMQ_Result.csv', index=False)





