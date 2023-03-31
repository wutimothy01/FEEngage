import numpy as np
import pandas as pd


def create_plan():
    current_stats = pd.read_csv("characterCurrentStats.csv")
    new_index= np.arange(1, len(current_stats) + 1)
    current_stats.index = new_index
    max_stats = pd.read_csv("characterMaxStats.csv", index_col="Name")
    max_class = pd.read_csv("classMaxStats.csv", index_col="Class")
    finished = dict()
    projects = dict()
    for row in current_stats.iterrows():
        current_stats_row = list(row[1])
        name = current_stats_row[0]
        picked_class = current_stats_row[1]
        max_stats_row = max_stats.loc[name]
        class_row = max_class.loc[picked_class]
        new_list = []
        new_list.append(int(class_row[0]))
        for i in range(1, len(class_row)-1):
            new_list.append(int(class_row[i]) + int(max_stats_row[i-1]))
        new_list.append(int(class_row[-1]))
        c_list = [int(i) for i in current_stats_row[2:]]
        d_list = [p_i - c_i for p_i, c_i in zip(new_list, c_list)]
        if sum(d_list) == 0:
            finished[name] = c_list
        else:
            projects[name+"Current"] = c_list
            projects[name+"Planned"] = new_list
            projects[name+"Difference"] = d_list
        
    column_name = ["HP", "Str", "Mag", "Dex", "Spd", "Def", "Res", "Lck", "Bld"]
    df = pd.DataFrame.from_dict(finished, orient='index', columns = column_name)
    df2 = pd.DataFrame.from_dict(projects, orient="index", columns=column_name)
    df.to_csv("finished.csv")
    df2.to_csv("projects.csv")


create_plan()