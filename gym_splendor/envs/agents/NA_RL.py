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
    # try:
    data = model[act]
    # except:
    #     print("lỗi action chưa có:",act)
    #     return state
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





class Agent(Player):
    with open(path + "envs/agents/model.json", 'r') as openfile:
        model = json.load(openfile)
    with open(path + "envs/agents/limit.json", 'r') as openfile:
        limit = json.load(openfile)
    with open(path + "envs/agents/value.json", 'r') as openfile:
        value = json.load(openfile)
    def __init__(self, name):
        super().__init__(name)
        self.pairs = []



    def action(self, dict_input):
        # print(self.amount_action_space)
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        list_score = [scoring(predict(State,act,Agent.model,Agent.limit),Agent.value) for act in list_action]
        score_sorted = list_score.copy()
        score_sorted.sort()
        sample_action = []
        capacity = 2
        for soluong in range(capacity):
            can_tim = score_sorted[soluong]
            indx = list_score.index(can_tim)
            sample_action.append(list_action[indx])
        action = random.choice(sample_action)
        print(len(sample_action))
        max_score = 0
        # dự đoán n turn sau đó
        turn_predict = 5
        old_state = State
        min_score = 99999
        for to_act in sample_action:
            for predicted in range(turn_predict):
                new_state = predict(old_state,to_act,Agent.model,Agent.limit)
                new_list_action = self.get_list_index_action(new_state)
                list_new_state = []
                for act in new_list_action:
                    list_new_state.append(predict(new_state,act,Agent.model,Agent.limit))
                    list_scores = [scoring(state_a,Agent.value) for state_a in list_new_state]
                best_score = min(list_scores)
                old_state = list_new_state[list_scores.index(best_score)]
            print(best_score)
            if best_score < min_score:
                min_score = best_score
                action = to_act
        self.pairs.append([State,action])
        # khi thắng, học value, model, limit
        if self.check_victory(State) == 1:
            try:
                with open(path + "envs/agents/value.json", 'r') as openfile:
                    value = json.load(openfile)
            except:
                value = {}
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
