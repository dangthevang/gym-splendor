import json

action = json.load(open('test/data_action.json'))

def convert_card_to_id(id):
    if 'Noble_' in id:
        return int(id.replace('Noble_', '')) + 90
    elif 'III_' in id:
        return int(id.replace('III_', '')) + 70
    elif 'II_' in id:
        return int(id.replace('II_', '')) + 40
    elif 'I_' in id:
        return int(id.replace('I_', ''))
def dich_arr(arr):
    cl = ['red', 'blue', 'green', 'white', 'black','auto_color']
    str_stock = []
    for i in arr:
        stock = [0,0,0,0,0,0]
        for sl in i:
            stock[cl.index(sl)] += 1
        str_stock.append(stock)
    return str_stock
def get_onl_hot_card(number):
    str_ = []
    for i in range(1, 91):
        if i == number:
            str_.append(1)
        else:
            str_.append(0)
    return str_
# for act in action:
#     print(act, action.index(act))
#     if type(act) == type(''):
#         print(get_onl_hot_card(convert_card_to_id(act)))
#     else:
#         print(dich_arr(act))
# n = int(input())
# ls = [int(input())for i in range(n)]
# print(ls)
a = [0, 1, 2, 5]
a = sorted(a)
print(a)
done = 0
min_ = a[0]
for i in a:
    if min_+1 < i:
        done = min_+1
        break
    min_ = i
    if done == 0:
        done = a[-1] + 1
print(done)
