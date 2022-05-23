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
    for id_state in range(len(state)):
        name = str(id_state) + "_" + str(state[id_state])
        if name in value.keys():
            score = value[name][0]
            list_score.append(score)
            # print(score,name)
    return min(list_score)





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
    def chosing_actions(self,State,mind_capacity):
        list_action = self.get_list_index_action(State)
        new_states = [predict(State,act,Agent.model,Agent.limit) for act in list_action]
        new_scores = [1/scoring(new_state,Agent.value) for new_state in new_states]
        chosen_actions = random.choices(list_action,weights=new_scores,k=mind_capacity)
        chosen_states = []
        for chosen_action in chosen_actions:
            chosen_states.append(new_states[list_action.index(chosen_action)])
        return chosen_actions, max(new_scores),chosen_states
    def chosing_new_states_from_many_states(self,list_state,mind_capacity):
        all_states = []
        all_scores = []
        for State in list_state:
            list_action = self.get_list_index_action(State)
            generated_states = [predict(State,act,Agent.model,Agent.limit) for act in list_action]
            generated_scores = [1/scoring(new_state,Agent.value) for new_state in generated_states]
            all_states += generated_states
            all_scores += generated_scores
        chosen_states = random.choices(all_states,weights=all_scores,k=mind_capacity)
        max_score = max(all_scores)
        return chosen_states,max_score

            # try:
        #     with open(path + "envs/agents/value.json", 'r') as openfile:
        #         self.value = json.load(openfile)
        # except:
        #     pass
    def action(self, dict_input):
        # print(self.amount_action_space)
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        action = random.choice(list_action)
        max_score = 0
        # dự đoán n turn sau đó
        turn_predict = 10
        # chọn ra n action để đệ quy
        mind_capacity = 2
        to_acts,score,chosen_states = self.chosing_actions(State,mind_capacity)
        old_states = [State]
        for act in to_acts:
            new_states = [predict(State,act,Agent.model,Agent.limit) for old_state in old_states]
            for turn_predicted in range(turn_predict):
                old_states,score = self.chosing_new_states_from_many_states(new_states,mind_capacity)
                new_states = old_states.copy()
                # print(turn_predicted,score,len(new_states))
            if score > max_score:
                max_score = score
                action = act
        print(max_score)   
        
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
