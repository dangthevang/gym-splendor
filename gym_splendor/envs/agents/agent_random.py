from re import T
from ..base.player import Player
import random
import math
import numpy as np
import json
path = "/content/gym-splendor/gym_splendor/"

def select(start,dict_model,limit):
    # try:
    max = limit[0]
    min = limit[1]
    selections = [a for a in dict_model.keys() if int(a) + start <= max and int(a) + start >= min]
    if len(selections) ==0:
        return 0
    weight = [dict_model[b] for b in selections]
    result = int(random.choices(selections,weights=weight)[0])
    return result
    # except:
    #     print(max,min,dict_model,selections,start)

def predict(state,act,model,limit):
    act_form = []
    data = model[act]
    for id_state in range(len(data)):
        act_form.append(select(state[id_state],data[id_state],limit[id_state]))
    new_state = np.array(state) + np.array(act_form)
    return list(new_state)

def scoring(state,value):
    list_score = []
    final = 1
    for id_state in range(len(state)):
        name = str(id_state) + "_" + str(state[id_state])
        if name in value.keys():
            score = value[name][0]
            # list_score.append(float(score))
            final *= score**(1/1000)
            # print(final,score)
            # print(score,name)
    return final

def find_n_smallest(list_n,n):
    mins = list_n[:n]
    mins.sort()
    for i in list_n[n:]:
        if i < mins[-1]: 
            mins.append(i)
            mins.sort()
            mins= mins[:n]
    return mins

class Agent(Player):
    # with open(path+"envs/agents/model.json", 'r') as openfile:
    #     model = json.load(openfile)
    # with open("/content/TienLenMienNam/gym_TLMN/envs/agents/limit.json", 'r') as openfile:
    #     limit = json.load(openfile)
    with open(path+"envs/agents/value.json", 'r') as openfile:
        value = json.load(openfile)
    def __init__(self, name):
        super().__init__(name)
        self.pairs = []
        # try:
        #     with open(path + "envs/agents/value.json", 'r') as openfile:
        #         self.value = json.load(openfile)
        # except:
        #     pass
    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        # print(State)
        print("điểm hiện tại",scoring(State,Agent.value))
        list_action = self.get_list_index_action(State)
        action = random.choice(list_action)
        # print(scoring(State,self.value))
        # model = Agent.model
        # limit = Agent.limit
        # min_score = 12
        # no_action = 5
        # # list_small_actions = random.choices(list_action,k=no_action)
        # if len(list_action) >1:
        #     for act in list_action:
        #         mode = 0
        #         old_states = [predict(State,act,model,limit)]
        #         for turn in range(min_score + 1):
        #             # print(turn)
        #             if mode == 1:
        #                 break
        #             new_states = []
        #             #check nếu đã xong game
        #             for old_state in old_states:
        #                 if self.check_victory(old_state) == 1:
        #                     mode = 1
        #                     break
        #                 # print(old_state)
        #                 generated_actions = self.get_list_index_action(old_state)
        #                 # actions = random.choices(generated_actions,k=no_action)
        #                 for to_act in generated_actions:
        #                     if to_act != 0:
        #                         new_states.append(predict(old_state,to_act,model,limit))
        #             old_states = new_states.copy()
        #         if turn <= min_score:
        #             min_score = turn
        #             action = act
        #     if min_score == 1:
        #         print("thắng mẹ rồi")
        #     else:
        #         print("dự kiến thắng sau",min_score-1,"turn nữa")        
        # print(State)
        # print(list_action)
        self.pairs.append([State,action])
        # khi thắng, học value, model, limit
        if self.check_victory(State) == 1:
            try:
                with open(path + "envs/agents/value.json", 'r') as openfile:
                    value = json.load(openfile)
            except:
                value = {"max":0}
            try:
                with open(path + "envs/agents/model.json", 'r') as openfile:
                    model = json.load(openfile)
            except:
                model = [[{} for _ in range(len(State))] for _ in range(self.amount_action_space)]
            try:
                with open(path + "envs/agents/limit.json", 'r') as openfile:
                    limit = json.load(openfile)
            except:
                limit = [[99999999999,0] for _ in range(len(State))]
            if len(self.pairs) > value["max"]:
                value["max"] = len(self.pairs)
            for id_pair in range(len(self.pairs)):
                old_state = self.pairs[id_pair][0]
                old_action = self.pairs[id_pair][1]
                if id_pair != len(self.pairs) -1:
                    new_state = self.pairs[id_pair+1][0]
                else:
                    new_state = State
                act_formula = np.array(new_state) - np.array(old_state)
                for id_state in range(len(act_formula)):
                    if old_state[id_state] < limit[id_state][1]:
                        limit[id_state][1] = old_state[id_state]
                    if old_state[id_state] > limit[id_state][0]:
                        limit[id_state][0] = old_state[id_state]
                    data = int(act_formula[id_state])
                    # print(old_action,id_state)
                    if data not in model[old_action][id_state].keys():
                        model[old_action][id_state][data] = 1
                    else:
                        model[old_action][id_state][data] += 1
                    name = str(id_state) + "_" + str(old_state[id_state])
                    if name not in value.keys():
                        value[name] = [len(self.pairs) - id_pair,1]
                    else:
                        data = value[name]
                        current_score = data[0]
                        current_times = data[1]
                        value[name] = [(current_score*current_times + len(self.pairs) - id_pair)/(current_times+1),current_times+1]
            with open(path+'envs/agents/model.json', 'w') as f:
                json.dump(model, f)
            with open(path+'envs/agents/limit.json', 'w') as f:
                json.dump(limit, f) 
            with open(path+'envs/agents/value.json', 'w') as f:
                json.dump(value, f)
        # khi thua, học model, limit
        if self.check_victory(State) == 0:
            try:
                with open(path + "envs/agents/model.json", 'r') as openfile:
                    model = json.load(openfile)
            except:
                model = [[{} for _ in range(len(State))] for _ in range(self.amount_action_space)]
            try:
                with open(path + "envs/agents/limit.json", 'r') as openfile:
                    limit = json.load(openfile)
            except:
                limit = [[0,9999999999] for _ in range(len(State))]
            for id_pair in range(len(self.pairs)):
                old_state = self.pairs[id_pair][0]
                old_action = self.pairs[id_pair][1]
                if id_pair != len(self.pairs) -1:
                    new_state = self.pairs[id_pair+1][0]
                else:
                    new_state = State
                act_formula = np.array(new_state) - np.array(old_state)
                for id_state in range(len(act_formula)):
                    if old_state[id_state] < limit[id_state][1]:
                        limit[id_state][1] = old_state[id_state]
                    if old_state[id_state] > limit[id_state][0]:
                        limit[id_state][0] = old_state[id_state]
                    data = int(act_formula[id_state])
                    # print(old_action,id_state)
                    if data not in model[old_action][id_state].keys():
                        model[old_action][id_state][data] = 1
                    else:
                        model[old_action][id_state][data] += 1
            with open(path+'envs/agents/model.json', 'w') as f:
                json.dump(model, f)
            with open(path+'envs/agents/limit.json', 'w') as f:
                json.dump(limit, f)       
        return action
