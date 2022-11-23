import requests
import json

from data import Data
import utils

# def return_ranks(accountNo : str, start_date : str, end_date : str, match_type : str, 
#                  n_players : int = 8, include_retire : bool = False, offset = 0, limit = 2):

# 기능 1 : 

ranks = utils.get_ranks(
    accountNo='973305538', startTime='2020-09-04T08:40:24', endTime='2022-09-04T08:40:24',
    matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', n_players = 4, limit = 100
    )
print(ranks)