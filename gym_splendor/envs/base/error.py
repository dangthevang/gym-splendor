from colorama import Fore, Back, Style
from gym_splendor.envs.agents import agents_inteface

def errorColor(name, message):
  print(Fore.RED + message, end='')
  print(Style.RESET_ALL)
  pass

def successColor(name, message):
  print(Fore.GREEN + name + ' ' + message, end='')
  print(Style.RESET_ALL)
  pass

def RecommendColor(message):
  print(Fore.YELLOW , message, end='')
  print(Style.RESET_ALL)
  pass