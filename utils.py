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
        
        def __str__(self):
            pass
        
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


def get_user_by_nickName(nickName, key = key):
    
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickName}',
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

def get_matchlist(accountNo, startTime, endTime, matchType, offset = 0, limit = 500):
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{accountNo}/matches?start_date={startTime}&end_date={endTime}&offset={offset}&limit={limit}&match_types={matchType}',
        headers=headers
    )
    
    return unpack_matchInfo(response.json())

# 기본기능 : 일정 기간의 순위 변동 그래프 (start_time, end_time, match_types)
def get_ranks(matchlist, n_players : list, include_retire : bool = False):
    ranks = []
    
    for match in matchlist:
        if match.playerCount in n_players:
            rank = int(match.player.matchRank)
            
            if rank == 99:
                if include_retire == True:
                    ranks.append(9)
            else:
                ranks.append(rank)
    
    return ranks

def get_relative_ranks(matchlist, include_retire: bool = False, include_single : bool = False):
    ranks = []
    
    for match in matchlist:
        rank = int(match.player.matchRank)
        if rank == 99:
            if include_retire == True:
                ranks.append(1)
        else:
            if match.playerCount == 1 and include_single == False:
                continue
            else:
                ranks.append(round(rank / match.playerCount, 2))
    
    return ranks

def get_channelNames(matchlist):
    # 채널 이름 : 횟수 의 Dictionary
    # mode 이름은 알파벳 오름차순 (a ~ z) -> count 내림차순으로 변경 요망
    
    modes = []
    for match in matchlist:
        modes.append(match.channelName)
        
    modes_set = list(set(modes))
    modes_set.sort()
    
    modecount = {}
    
    for mode in modes_set:
        modecount[mode] = 0
    
    for mode in modes:
        modecount[mode] += 1
    
    return modecount

def plot_ranks(ranks : list, n_players : int = 8):
    """display rank graph
    
    Args:
        ranks (list): list with ranks, elements are integer between 1 ~ n_players
        n_players (int): maximum players (default = 8)
        include_retire (bool, optional): Defaults to False (Not include Retire), True(interpret Retire as n_players + 1)
    """

    ranks = [i for i in ranks if i != 99]
    
    x = np.linspace(1, len(ranks)+1, len(ranks))
    y = ranks
    plt.plot(x, y)
    plt.gca().invert_yaxis() # 1등이 높은 순위이므로 y축의 scale을 반대로 변경
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
    
    # basic test of get_user
    
    #user = get_user_by_nickName('MOOOMOO'); print(user.name)
    #user = get_user_by_accountNo(user.accountNo); print(user.name)
    
    # test matchlist
    
    #matchlist = get_matchlist(
    #    accountNo=user.accountNo, startTime='2020-09-04T08:40:24', endTime='2022-09-04T08:40:24',
    #    matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', limit = 100
    #    )
    
    #for match in matchlist:
    #    print(match)
    
    # test return_ranks
    # def return_ranks(accountNo : str, start_date : str, end_date : str, match_type : str, n_players : int = 8, include_retire : bool = False, offset = 0, limit = 2):
    #ranks = get_ranks(
    #    accountNo='973305538', startTime='2020-09-04T08:40:24', endTime='2022-09-04T08:40:24',
    #    matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', n_players = 8, limit = 100
    #    )
    
    # test return_relative_ranks
    #def return_relative_ranks(accountNo : str, start_date : str, end_date : str, match_type : str, 
    #                     include_single : bool = False, include_retire : bool = False, offset = 0, limit = 2):
    #ranks = get_relative_ranks(
    #    accountNo='973305538', startTime='2020-09-04T08:40:24', endTime='2022-09-04T08:40:24',
    #    matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', include_single = False, 
    #    include_retire = False, limit = 100
    #    )
    

    matchlist = get_matchlist(accountNo='973305538', startTime='2018-09-04T08:40:24', endTime='2022-09-04T08:40:24',
        matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a')
    
    print(get_channelNames(matchlist))
    
    
    # # def get_ranks(matchlist, n_players : list, include_retire : bool = False):
    # ranks = get_ranks(matchlist, [1, 2, 3, 4, 5, 6, 7, 8], include_retire=False)
    
    # # def get_relative_ranks(matchlist, include_retire: bool = False, include_single : bool = False):
    # ranks = get_relative_ranks(matchlist, include_retire=False, include_single=False)
    
    # test plot_ranks
    # plot_ranks(ranks, 8)