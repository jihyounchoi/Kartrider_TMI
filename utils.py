import requests
import json
import matplotlib.pyplot as plt
import numpy as np

key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6Ijk3MzMwNTUzOCIsImF1dGhfaWQiOiIyIiwiZXhwIjoxNjgzMTkwNDYyLCJpYXQiOjE2Njc2Mzg0NjIsIm5iZiI6MTY2NzYzODQ2Miwic2VydmljZV9pZCI6IjQzMDAxMTM5MyIsInRva2VuX3R5cGUiOiJBY2Nlc3NUb2tlbiJ9.o4oNGosgyTmNuSt752GBIFQMozxKYkPLDkfGEKEEBMk'

def get_user_by_name(nickname, key = key):
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickname}',
        headers=headers
    )
    return response.json()

def get_user_by_accessId(accessId, key = key):
    """get user nickname by access id

    Args:
        accessId (int, string): _description_
        key (access key, optional): _description_. Defaults to key.

    Returns:
        response in json type
    """
    if type(accessId) != 'str':
        accessId = str(accessId)
    
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{accessId}',
        headers=headers
    )
    return response.json()

# continue...
def get_matchlist(accessId, start_date, end_date, match_type, offset = 0, limit = 2):
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{accessId}/matches?start_date={start_date}&end_date={end_date}&offset={offset}&limit={limit}&match_types={match_type}',
        headers=headers
    )
    
    # return example
    '''
    {'matches': 
    [
        {
            'matches': [
                {'accountNo': '973305538', 'matchId': '0339000be9fc8591', 'matchType': '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', 'teamId': '0', 'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 'startTime': '2022-09-04T08:40:24', 'endTime': '2022-09-04T08:42:07', 'channelName': 'speedIndiCombine', 'trackId': '3c03b354c083aa8311b62221f535b6228f935e9b3a9352b0f2c1c71ac7833544', 'playerCount': 8, 'matchResult': '1', 'seasonType': '', 'player': {'accountNo': '', 'characterName': '', 'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 'kart': '751a4dd7b0e66ba60c3feb72191980bfed2eac7068930521c59171a514fff837', 'license': '', 'pet': '', 'flyingPet': '13e247466d75204e1b3d587abcc11def087f6ffcdfcf798cb2c4b8edcddd8f5b', 'partsEngine': '', 'partsHandle': '', 'partsWheel': '', 'partsKit': '', 'rankinggrade2': '5', 'matchRank': '1', 'matchRetired': '0', 'matchWin': '1', 'matchTime': '81730'}}, 
                {'accountNo': '973305538', 'matchId': '02ca000d4c00cd87', 'matchType': '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', 'teamId': '0', 'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 'startTime': '2022-07-07T16:33:37', 'endTime': '2022-07-07T16:35:24', 'channelName': 'speedIndiInfinit', 'trackId': '929803c3549892072d76bea9fbe5811424146ac8a5ba3ffd91741c50ff06a9a8', 'playerCount': 7, 'matchResult': '0', 'seasonType': '', 'player': {'accountNo': '', 'characterName': '', 'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 'kart': 'f6799591217651d8f449a7877f70d21bcd344687575ef44f3ca3230aa40e8ba3', 'license': '', 'pet': '', 'flyingPet': '13e247466d75204e1b3d587abcc11def087f6ffcdfcf798cb2c4b8edcddd8f5b', 'partsEngine': '', 'partsHandle': '', 'partsWheel': '', 'partsKit': '', 'rankinggrade2': '5', 'matchRank': '2', 'matchRetired': '0', 'matchWin': '0', 'matchTime': '85243'}}
        ]
    , 'matchType': '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a'}], 'nickName': 'MOOOMOO'
    }
    '''
    
    return response.json()  

# 기본기능 : 일정 기간의 순위 변동 그래프 (start_time, end_time, match_types)
def return_ranks(accessId : str, start_date : str, end_date : str, match_type : str, offset = 0, limit = 2):
    ranks = []
    matches = get_matchlist(accessId, start_date, end_date, match_type = match_type, offset = offset, limit = limit)
    matches = matches['matches'][0]['matches']
    
    for i in range(len(matches)):
        ranks.append(matches[i]['player']['matchRank'])
    
    return ranks

def plot_ranks(ranks : list, n_players):
    # 리타이어의 경우는 99로 표기되므로, 이를 적절히 표기하는 것이 중요
    # 1등이 높은 것이므로, y axis를 반대로 표기해야 함
    

################### test code #####################

if __name__ == '__main__':
    # Test Environment
    # accessId = '973305588'
    # start_date = '2021-09-04T08:40:24'
    # end_date = '2022-09-04T08:40:24'
    # match_type = '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a'

    user = get_user_by_name('MOOOMOO'); print(user['name'])
    user = get_user_by_accessId(user['accessId']); print(user['name'])
    
    matchlist = get_matchlist(
        accessId=user['accessId'], start_date='2021-09-04T08:40:24', end_date='2022-09-04T08:40:24', \
        match_type='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', limit=2
        )
    
    # print(matchlist)
    
    ranks = return_ranks(
        accessId='973305538', start_date='2021-09-04T08:40:24', end_date='2022-09-04T08:40:24', \
        match_type='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', limit = 200
        )
    
    print(ranks)