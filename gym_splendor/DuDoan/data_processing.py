import pandas as pd
import json


def str2dict(string, target):
  string = string.replace("\'", "\"")
  json_object = json.loads(string)
  return json_object[target]


def arr2str(arr):
  arr = arr.replace('[', '')
  arr = arr.replace(']', '')
  return arr


def arr2dict(arr, target):
  string = arr2str(arr)
  obj = str2dict(string, target)
  return obj


def get_player_name_repectively(dat, ids):
  name_index = dat['player name'].iloc[0]
  name_index = name_index.replace('[', '')
  name_index = name_index.replace(']', '')
  name_index = name_index.replace("'", '')
  name_index = name_index.replace('"', '')
  name_index = name_index.replace(" ", "")
  name_index_ = name_index.split(',')
  return name_index_[ids]


def ger_score_repectively(string, ids):
  name_index = string
  name_index = name_index.replace('[', '')
  name_index = name_index.replace(']', '')
  name_index = name_index.replace("'", '')
  name_index = name_index.replace('"', '')
  name_index = name_index.replace(" ", "")
  name_index_ = name_index.split(',')
  return int(name_index_[ids])


def player_stocks_value_repectively(string, ids_player, color_stock):
  stocks = ['red', 'blue', 'green', 'white', 'black', 'auto_color']
  ids_stock = stocks.index(color_stock)
  values = string.replace("dict_values", '')
  values = values.replace('[', '')
  values = values.replace(']', '')
  values = values.split('),')
  # values
  new_values = []
  for v in values:
    v = v.replace('(', '')
    v = v.replace(')', '')
    v = v.replace(' ', '')
    v = v.split(',')
    new_values.append(v)
  return new_values[ids_player][ids_stock]


def one_arr2int(arr):
  arr = arr.replace('[', '')
  arr = arr.replace(']', '')
  return int(arr)


def split_name_from_col(col_name):
  col_name_lst = col_name.split('_')
  return col_name_lst[1]


def replace_string_in_col(col_name, target_replace, target_result):
  """
  col_name : name of column that want to rename
  target_replace: string that wanna replace ( name only )
  target_result: string that wanna after replace
  """
  return col_name.replace(target_replace, target_result)


def rename_column(data, col_name_repectively):
  dict_rename = {}
  dict_string_rename = {}
  for col_name in col_name_repectively:
    dict_string_rename[col_name] = 'player{}'.format(col_name_repectively.index(col_name))
  # print('dict rename ', dict_string_rename)

  columns = data.columns
  for col in columns:
    for name in col_name_repectively:
      if name in col:
        # print('col before ', col)
        dict_rename[col] = col.replace(name, dict_string_rename[name])
        # print('col after ', col)
  data = data.rename(columns=dict_rename)
  return data


def clean_data(dat):
  # board stocks
  dat['board_stocks_red'] = [arr2dict(i, "red") for i in dat['board stocks']]
  dat['board_stocks_blue'] = [arr2dict(i, "blue") for i in dat['board stocks']]
  dat['board_stocks_green'] = [arr2dict(i, "green") for i in dat['board stocks']]
  dat['board_stocks_white'] = [arr2dict(i, "white") for i in dat['board stocks']]
  dat['board_stocks_black'] = [arr2dict(i, "black") for i in dat['board stocks']]
  dat['board_stocks_auto_color'] = [arr2dict(i, "auto_color") for i in dat['board stocks']]
  dat = dat.drop(columns=['board stocks'])
  # player score
  col_name_repectively = [get_player_name_repectively(dat, i) for i in range(4)]
  for ids in range(4):
    dat['player_score_' + col_name_repectively[ids]] = [ger_score_repectively(i, ids) for i in dat['player score']]

  # player stocks value
  for ids_player in range(4):
    for color in ['red', 'blue', 'green', 'white', 'black', 'auto_color']:
      col_name = 'player_' + col_name_repectively[ids_player] + '_stock_' + color
      dat[col_name] = [player_stocks_value_repectively(i, ids_player, color) for i in dat['player stocks value']]

  # card open
  col_name_lst = []
  for name in col_name_repectively:
    col_name = 'player_' + name + '_card_open'
    dat[col_name] = dat['player card open']
    col_name_lst.append(col_name)

  for col_name in col_name_lst:
    dat[col_name] = dat[col_name].apply(lambda x: str2dict(x, split_name_from_col(col_name)))

  # turn
  dat['Turn'] = [one_arr2int(i) for i in dat['turn']]
  dat = dat.drop(columns=['player card open', 'player stocks value', 'player score', 'turn'])

  # rename column
  dat = rename_column(dat, col_name_repectively)
  return dat


def main():
    for ban in range(1000):
        raw_dat = pd.read_csv('gym_splendor/DuDoan/Raw_data/dat{}.csv'.format(ban))
        clean_dat = clean_data(raw_dat)
        clean_dat.to_csv('gym_splendor/DuDoan/Clean_data/dat{}.csv'.format(ban))
        if ban % 100 == 0:
          print('processing {}%'.format(ban/1000 * 100))

def merge_data():
  pass

if __name__ == '__main__':
  main()