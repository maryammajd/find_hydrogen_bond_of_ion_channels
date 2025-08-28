import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import pdb;pdb.set_trace()
import json, os, ast

def mean_value(data, mean_step):
    mean_data = []
    for i in range(1, int((len(data)-1)/mean_step)+1):
        mean_data.append(np.mean(data[(i-1)*mean_step:i*mean_step]))
    return mean_data

def save_all_pairs(source_dir, simulation_dir, VSD):
    pair_distance = {}
    filenames = []
    sims = simulation_dir
    for sim in sims:
        filename = f"{source_dir}/outputs/{sim}-dist-all-{VSD}.xvg"
        filenames.append(filename)
    dict_of_df = OrderedDict()
    for sim_complete_dir in filenames:
        # print(sim)
        dict_of_df[sim_complete_dir.split('/')[-1].split('-dist')[0]] = pd.read_csv(sim_complete_dir, skiprows=18, header=None) 
        
    return dict_of_df

import sys

if len(sys.argv) < 2:
    print("Usage: plot_percentage_of_bonds.py domains_to_check \( in form of array \[DOMAIN1, DOMAIN2\]\) csv_file_containing_simulations")
    sys.exit(1)

domains = sys.argv[1]
dataframe_info = pd.read_csv(sys.argv[2], delimiter=',', index_col=0)
VSDs =  ast.literal_eval(domains)
source_dir = os.getcwd()

def percentage_h_bonds(dict_of_dist):
    percentage = {}
    for pair_num in dict_of_dist.keys()[1:]:
        h_bonds = []
        for dist in range(int(len(dict_of_dist[pair_num])/2), len(dict_of_dist[pair_num])):
            h_bonds.append(dict_of_dist[pair_num][dist] < 0.35)
        percentage[pair_num] = sum(h_bonds) / len(h_bonds)
    return percentage


with open(f"inputs/source_model.gro", "r") as gro_file:
    gro_lines = gro_file.readlines()[1:]
# print(gro_lines[1])

simulation_dir = dataframe_info.index
percentage_all_bonds, percentage_bonds = {}, {}
for VSD in VSDs:
    percentage_all_bonds[VSD], percentage_bonds[VSD] = {}, {}
    with open(f"outputs/H-bond_pairs_{VSD}.ndx", "r") as txt_file:
        pairs_index = ['time']
        for ln in txt_file:
            if not ln.startswith("["):
                pairs_index.append(ln[:-1])


        all_pairs = save_all_pairs(source_dir, simulation_dir, VSD)
    print(VSD)
    pair_int = {} 
    for sim_num, sim_name in enumerate(all_pairs.keys()):
        print(sim_name)
        if sim_num == 0:
            eq_source = sim_name
        percentage_all_bonds[VSD][sim_name] = percentage_h_bonds(all_pairs[sim_name])
        key_stable = [key for key,per in percentage_all_bonds[VSD][eq_source].items() if per > 0.5]  
        
        percentage_bonds[VSD][sim_name] = {key : percentage_all_bonds[VSD][sim_name][key] for  key in key_stable}
        # print('***\n', sim_name, len(kept_bonds))
        # print('---------------\n', loosed_bonds)
    print(percentage_bonds[VSD])
    for key_1, values in percentage_bonds[VSD].items():
        print(key_1)
        for key_2, value in values.items():
            if value < 0.5:
                print(key_1, key_2, value)
                
    for simul_name in percentage_bonds[VSD].keys():
        if not simul_name == eq_source:
            lost_bonds_for_sim = {i:percentage_bonds[VSD][simul_name][i] for i in percentage_bonds[VSD][simul_name].keys() if percentage_bonds[VSD][simul_name][i] < 0.5}
            x_index = (lost_bonds_for_sim).keys()
            x_pos = np.arange(len(x_index))
            x_values = [str(gro_lines[int(pairs_index[item].split()[0])][:5]) +'-'+ str(gro_lines[int(pairs_index[item].split()[1])][:5]) for item in np.array(list(x_index))]

            y_values = [lost_bonds_for_sim[i] for i in lost_bonds_for_sim.keys()]
            y_values_eq = [percentage_bonds[VSD][eq_source][i] for i in lost_bonds_for_sim.keys()]
            num_sims = len(lost_bonds_for_sim.keys())
            plt.figure(figsize=(16, 12))
                # Adjust x positions for grouped bars
            plt.bar(x_pos, y_values, 0.4, capsize=5, label=simul_name, alpha=0.8, color = dataframe_info['color'][simul_name])
            plt.bar(x_pos + 1 * 0.41, y_values_eq, 0.4, capsize=5, label='eq', alpha=0.8, color = dataframe_info['color'][simulation_dir[0]])
            plt.axhline(y=0.5)
            # Labels and title
            plt.xticks(x_pos + 0.2, x_values, rotation=90)  # Center xticks
            plt.xlabel("X values")
            plt.ylabel("Y values")
            name_sim = simul_name.split('/')[-1]
            plt.title(f"lost H-bonds in eq. and {name_sim}")
            plt.legend()
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.savefig(f'outputs/lost_bonds_{name_sim}-{VSD}.png')
            # Show plot
            # plt.show()
            plt.close()

