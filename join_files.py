import pandas as pd
import os


def results_concat(path_in, path_out, group): 
    files = [os.path.join(path_in, file) for file in os.listdir(path_in) if '.csv' in file]
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df["group"] = group
    return df.to_csv(os.path.join(path_out,f"results_{group}.csv"), index=False)



def all(path):
    name_folder = [folder for folder in os.listdir(path) if "." not in folder]
    folders = [os.path.join(path, folder) for folder in os.listdir(path) if "." not in folder]
    count = 0
    for i in folders:
        files = [os.path.join(i, file) for file in os.listdir(i) if '.csv' in file]
        df = pd.concat(map(pd.read_csv, files), ignore_index=True)
        df["group"] = name_folder[count]
        df.to_csv(os.path.join(path, f"all_{name_folder[count]}.csv"), index=False)  
        count += 1
    fil = [os.path.join(path, file) for file in os.listdir(path) if '.csv' in file]
    frame = pd.concat(map(pd.read_csv, fil), ignore_index=True)
    return frame.to_csv(os.path.join(path, "all_.csv"), index=False)


# all("C:/Users/jhons/Desktop/resultados")