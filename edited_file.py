'''
Module to edit big file with films
'''

import csv

def read_file(path: str) -> list :
    """
    Return list of lines from file
    """
    with open(path, 'r',encoding='utf-8',errors='ignore') as file:
        contain = file.readlines()
        split_words(contain)

def split_words(contain):
    '''
    Edit lines to more appropriate and write it in file
    '''
    new_doc = []
    with open('new_list.csv', 'w') as f:
        writer = csv.writer(f)
        for line in contain:
            splited_by_tab = line.split('	')
            if splited_by_tab[0].find('}') != -1:

                name_and_year, another_info = splited_by_tab[0].split(' {')
                name, year = name_and_year.split('" ')
            else:
                name, year = splited_by_tab[0].split('" ')
            if splited_by_tab[-1].find('(') == -1:
                place = splited_by_tab[-1]
            else:
                place = splited_by_tab[-2]
            name = name.replace('"', '')
            place = place.replace('\n' , '')
            place = place.replace("'", '')
            writer.writerow((name, year, place))
    return new_doc


read_file('locations.list')
