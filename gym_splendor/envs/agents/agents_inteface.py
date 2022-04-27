import random
from gym_splendor.envs.agents import agent_Phong as a1
from gym_splendor.envs.agents import agent_Ann as a2
from gym_splendor.envs.agents import agent_Hieu as a3
from gym_splendor.envs.agents import agent_HungThom as a4
from gym_splendor.envs.agents import agent_MA as a5
from gym_splendor.envs.agents import agent_NA as a6
from gym_splendor.envs.agents import agent_Trang as a7
from gym_splendor.envs.agents import agent_Hieuuu as a8
from gym_splendor.envs.agents import agent_random as a9

temp = [a1.Agent("Gió"),a2.Agent("Ann"),a3.Agent("Híu"),a4.Agent("HTc"), a5.Agent('miA'), a6.Agent('Sếp'), a7.Agent('Trn'), a8.Agent('Hýu'), a9.Agent('Ran')]
random.shuffle(temp)
ListPlayer = temp

# from gym_splendor.envs.agents import agent_Hieuuu as a1
# from gym_splendor.envs.agents import agent_Hieuuu as a2
# from gym_splendor.envs.agents import agent_Hieuuu as a3
# from gym_splendor.envs.agents import agent_Hieuuu as a4

# ListPlayer = [a1.Agent("P1"),a2.Agent("P2"),a3.Agent("P3"),a4.Agent("P4")]