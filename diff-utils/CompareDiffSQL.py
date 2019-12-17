import os
import os.path
import filecmp

base_folder = "base_source/resources"
layer_list = ['layer_1', 'layer_2']
path_list = ['scripts/folder_1', 'scripts/folder_2', 'scripts/folder_3', 'scripts/folder_3']


def read_layers(layer_name, paths):
    file_dict = dict()
    for path_name in paths:
        file_dict[path_name] = []
        for dirpath, dirnames, filenames in os.walk(base_folder + "/" + layer_name + "/" + path_name):
            for filename in [f for f in filenames if f.endswith(".sql")]:
                file_dict[path_name].append(filename)

    return file_dict


def compare_list(path, list1, list2, layers):
    difference_dict = {}
    difference_dict['onlyInList1'] = []
    difference_dict['onlyInList2'] = []

    for el in list1:
        if el in list2:
            name1 = base_folder + "/" + layers[0] + "/" + path + "/" + el
            name2 = base_folder + "/" + layers[1] + "/" + path + "/" + el
            if not filecmp.cmp(name1, name2):
                print("Following files are not equals")
                print(name1)
                print(name2)
                print(' ')


layer_dict = dict()
for layer in layer_list:
    file_dict = read_layers(layer, path_list)
    layer_dict[layer] = file_dict

for element in path_list:
    print('for ' + element)
    compare_list(element, layer_dict[layer_list[0]].get(element), layer_dict[layer_list[1]].get(element), layer_list)
    print('###')
    print('###')

