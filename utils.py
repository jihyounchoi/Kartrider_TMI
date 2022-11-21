import requests
import json
import matplotlib.pyplot as plt
import numpy as np

key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6Ijk3MzMwNTUzOCIsImF1dGhfaWQiOiIyIiwiZXhwIjoxNjgzMTkwNDYyLCJpYXQiOjE2Njc2Mzg0NjIsIm5iZiI6MTY2NzYzODQ2Miwic2VydmljZV9pZCI6IjQzMDAxMTM5MyIsInRva2VuX3R5cGUiOiJBY2Nlc3NUb2tlbiJ9.o4oNGosgyTmNuSt752GBIFQMozxKYkPLDkfGEKEEBMk'

# {'accountNo': '', 
# 'characterName': '', 
# 'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 
# 'kart': '751a4dd7b0e66ba60c3feb72191980bfed2eac7068930521c59171a514fff837', 
# 'license': '', 
# 'pet': '',
# 'flyingPet': '13e247466d75204e1b3d587abcc11def087f6ffcdfcf798cb2c4b8edcddd8f5b', 
# 'rankinggrade2': '5', 
# 'matchRank': '1', 
# 'matchRetired': '0', 
# 'matchWin': '1', 
# 'matchTime': '81730',
 
class Player():
    def __init__(self, accountNo, characterName, character, kart, license, pet, flyingPet, 
                 rankinggrade2, matchRank, matchRetired, matchWin, matchTime):
        self.accountNo = accountNo
        self.characterName = characterName
        self.character = character
        self.kart = kart
        self.license = license
        self.pet = pet
        self.flyingPet = flyingPet
        self.rankinggrade2 = rankinggrade2
        self.matchRank = matchRank
        self.matchRetired = matchRetired
        self.matchWin = matchWin
        self.matchtime = matchTime

# 'accountNo': '973305538', 
# 'matchId': '0339000be9fc8591', 
# 'matchType': '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', 
# 'teamId': '0', 
# 'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 
# 'startTime': '2022-09-04T08:40:24', 
# 'endTime': '2022-09-04T08:42:07', 
# 'channelName': 'speedIndiCombine', 
# 'trackId': '3c03b354c083aa8311b62221f535b6228f935e9b3a9352b0f2c1c71ac7833544', 
# 'playerCount': 8, 
# 'matchResult': '1', 
# 'seasonType': '',

class Match():
    
    def __init__(self, accountNo, matchId, matchType, teamId, character, startTime, 
                 endTime, channelName, trackId, playerCount : int, matchResult, nickName,
                 player_accountNo, player_characterName, player_character, player_kart,
                 player_license, player_pet, player_flyingPet, player_rankinggrade2,
                 player_matchRank, player_matchRetired, player_matchWin, player_matchTime) -> None:
        self.accountNo = accountNo
        self.matchId = matchId
        self.matchType = matchType
        self.teamId = teamId
        self.character = character
        self.startTime = startTime
        self.endTime = endTime
        self.channelName = channelName
        self.trackId = trackId
        self.playerCount = playerCount
        self.matchResult = matchResult
        self.nickName = nickName
        self.player = Player(player_accountNo, player_characterName, player_character, player_kart, player_license, player_pet,
                             player_flyingPet, player_rankinggrade2, player_matchRank, player_matchRetired, player_matchWin, player_matchTime)
        
class User():
    def __init__(self, accountNo, name, level) -> None:
        self.accountNo = accountNo
        self.name = name
        self.level = level
        
def unpack_matchInfo(matches) -> list:
    
    nickName = matches['nickName']
    matches = matches['matches'][0]['matches']
    
    print(type(matches))
    result = []
    
    for i in range(len(matches)):
        
        match = matches[i]
        player = matches[i]['player']
        
        match_instance = Match(match['accountNo'], match['matchId'], match['matchType'], match['teamId'], match['character'], match['startTime'],
                               match['endTime'], match['channelName'], match['trackId'], match['playerCount'], match['matchResult'], nickName,
                               player['accountNo'], player['characterName'], player['character'], player['kart'], player['license'], player['pet'], player['flyingPet'], 
                               player['rankinggrade2'], player['matchRank'], player['matchRetired'], player['matchWin'], player['matchTime'])
        
        result.append(match_instance)
        
    return result

def unpack_userInfo(user):
    user_instance = User(user['accessId'], user['name'], user['level'])
    return user_instance


def get_user_by_name(nickname, key = key):
    
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickname}',
        headers=headers
    )
    
    print(response.json())
    
    return unpack_userInfo(response.json())

def get_user_by_accountNo(accountNo, key = key):
    """get user nickname by accountNo (= accessId)

    Args:
        accountNo (int, string): _description_
        key (access key, optional): _description_. Defaults to key.

    Returns:
        response in json type
    """
    if type(accountNo) != 'str':
        accountNo = str(accountNo)
    
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{accountNo}',
        headers=headers
    )
    return unpack_userInfo(response.json())

def get_matchlist(accountNo, start_date, end_date, match_type, offset = 0, limit = 2):
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{accountNo}/matches?start_date={start_date}&end_date={end_date}&offset={offset}&limit={limit}&match_types={match_type}',
        headers=headers
    )
    
    return unpack_matchInfo(response.json())

# 기본기능 : 일정 기간의 순위 변동 그래프 (start_time, end_time, match_types)
def return_ranks(accountNo : str, start_date : str, end_date : str, match_type : str, offset = 0, limit = 2):
    ranks = []
    matches = get_matchlist(accountNo, start_date, end_date, match_type = match_type, offset = offset, limit = limit)
    
    for match in matches:
        ranks.append(match.player.matchRank)
    
    return ranks

def plot_ranks(ranks : list, n_players, include_retire : bool = False):
    # 리타이어의 경우는 99로 표기되므로, 이를 적절히 표기하는 것이 중요
    # 현재 구현 버전은 리타이어 기록을 아예 제거함
    # 1등이 높은 것이므로, y axis를 반대로 표기해야 함
    # 2명중 1명과 8명중 1명이 동일한 순위이므로, 이를 반영한 상대 수치가 필요
    
    ranks = list(map(int, ranks))

    if include_retire == False: # exclude retire
        ranks = [i for i in ranks if i != 99]
        
    else: # manage retire as n_players + 1 (8 players -> 9)
        for i in range(len(ranks)):
            if ranks[i] == 99:
                ranks[i] = 9
    
    x = np.linspace(1, len(ranks)+1, len(ranks))
    y = ranks
    plt.plot(x, y)
    plt.gca().invert_yaxis()
    plt.show()
    
    
    
    

################### test code #####################

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

if __name__ == '__main__':
    # Test Environment
    # accountNo = '973305588'
    # start_date = '2021-09-04T08:40:24'
    # end_date = '2022-09-04T08:40:24'
    # match_type = '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a'
    
    # basic get_user test
    user = get_user_by_name('MOOOMOO'); print(user.name)
    user = get_user_by_accountNo(user.accountNo); print(user.name)
    
    matchlist = get_matchlist(
        accountNo=user.accountNo, start_date='2021-09-04T08:40:24', end_date='2022-09-04T08:40:24', \
        match_type='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', limit=2
        )
    
    for match in matchlist:
        print(match.matchId)
    
    ranks = return_ranks(
        accountNo='973305538', start_date='2021-09-04T08:40:24', end_date='2022-09-04T08:40:24', \
        match_type='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', limit = 200
        )
    
    plot_ranks(ranks, 8, include_retire=True)