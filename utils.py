import requests
import json
from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np

# api 요청시 포함하는 key
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6Ijk3MzMwNTUzOCIsImF1dGhfaWQiOiIyIiwiZXhwIjoxNjgzMTkwNDYyLCJpYXQiOjE2Njc2Mzg0NjIsIm5iZiI6MTY2NzYzODQ2Miwic2VydmljZV9pZCI6IjQzMDAxMTM5MyIsInRva2VuX3R5cGUiOiJBY2Nlc3NUb2tlbiJ9.o4oNGosgyTmNuSt752GBIFQMozxKYkPLDkfGEKEEBMk'

#### Player() instance example ####
# 'accountNo': '', 
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

#### Match() instance example ####
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
    """
    get_matchlist 계열의 함수에서 내부적으로 사용하는 함수입니다.
    API를 통해 불러온 json 형태의 객체를 unpack하여 Match class의 객체로 저장합니다.
    return 형은 list로, Match class의 객체들을 원소로 가집니다.

    Args:
        matches : json-form instance

    Returns:
        list: list[Match()]
    """
    
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
    """
    get_user 계열의 함수에서 내부적으로 사용하는 함수입니다.
    API를 통해 불러온 json 형태의 객체를 unpack하여 User class의 객체로 저장합니다.
    return 형은 list로, User class의 객체들을 원소로 가집니다.

    Args:
        matches : json-form instance

    Returns:
        User : User() instance
    """
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

def get_matchlist(accountNo : str, startTime : str, endTime : str, matchType : str, offset = 0, limit = 500):
    """
    accountNo, matchType에 해당하는 startTime ~ endTime 간의 경기 결과를 API를 통해 조회합니다.
    limit의 default 값은 500이며, 더 큰 값을 지정해도 500건까지만 조회 가능합니다.
    startTime과 endTime에 관계없이 최근 1년간의 데이터만 유효합니다.

    Args:
        accountNo (str): 유저의 고유번호를 의미합니다. get_user_by_nickname() 함수를 통해 닉네임에서 accountNo를 조회 가능합니다.
        startTime (str): 경기의 시작 시간을 의미합니다. 최근 1년까지만 유효합니다. ex) '2022-09-03T08:40:24'
        endTime (str): 경기의 종료 시간을 의미합니다. 최근 1년까지만 유효합니다. ex) '2022-09-04T08:40:24'
        matchType (str): 매치 타입을 의미하는 고유 아이디입니다. data.py에서 아이디와 이름을 조회할 수 있습니다.
        offset (int, optional): 내부 변수. Defaults to 0.
        limit (int, optional): 가져오고자 하는 매치의 총 개수를 의미합니다. 최대 500까지만 가능합니다. Defaults to 500.

    Returns:
        list[Match()]: Match class의 instance로 이루어진 리스트를 리턴합니다.
    """
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{accountNo}/matches?start_date={startTime}&end_date={endTime}&offset={offset}&limit={limit}&match_types={matchType}',
        headers=headers
    )
    
    print(response.json())
    
    return unpack_matchInfo(response.json())
    
def get_matchInfo(matchId : str):
    """
    특정 matchId에 해당하는 세부 매치 결과를 리턴합니다.
    아직까지는 json 객체를 따로 unpack하지 않고 그대로 리턴하는 형태까지만 구현되어 있습니다.

    Args:
        matchId (str): get_matchlist를 통해 조회된 matchId를 의미합니다.

    Returns:
        json: json 형태의 match 결과를 리턴합니다.
    """
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/matches/{matchId}',
        headers=headers
    )
    
    return response.json()

# 기본기능 : matchlist 객체를 받으면, rank 정보 추출
def get_ranks(matchlist : list, n_players : list, include_retire : bool = False) -> list:
    """
    Match객체로 이루어진 matchlist를 입력으로 받은 후, 순위 정보만을 추출하여 list 형태로 리턴합니다.

    Args:
        matchlist (list): Match() 객체로 이루어진 list입니다. get_matchlist의 리턴형과 동일합니다.
        n_players (list): 결과에 포함하고자 하는 총 플레이어의 수를 의미합니다. n_players = [8]인 경우, 8명이 참여한 경기에서의 순위만을 포함합니다.
        include_retire (bool, optional): 리타이어한 경기의 순위를 포함하는지를 의미합니다. default는 False이며, True시 9등으로 처리합니다.

    Returns:
        list: 경기에서의 순위를 원소로 가지는 list 객체를 리턴합니다.
    """
    ranks = []
    
    for match in matchlist:
        
        # and 뒤의 부분 : 간혹 matchRank가 공란인 경우가 있어서 (강제종료), 해당 예외를 처리하기 위한 구문입니다.
        if (match.playerCount in n_players) and (match.player.matchRank in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '99']): 
            
            rank = int(match.player.matchRank)
            
            if rank == 99:
                if include_retire == True:
                    ranks.append(9)
            else:
                ranks.append(rank)
    
    return ranks

def get_relative_ranks(matchlist, n_players : list, include_retire: bool = False) -> list:
    """
    get_ranks와 유사하지만, (자신의 등수 / 참여한 플레이어 수)로 계산된 상대 순위를 리턴합니다.

    Args:
        matchlist (list): Match() 객체로 이루어진 list입니다. get_matchlist의 리턴형과 동일합니다.
        n_players (list): 결과에 포함하고자 하는 총 플레이어의 수를 의미합니다. n_players = [8]인 경우, 8명이 참여한 경기에서의 순위만을 포함합니다.
        include_retire (bool, optional): 리타이어한 경기의 순위를 포함하는지를 의미합니다. True인 경우 1로 처리하며, Default는 False입니다.

    Returns:
        list: relative_rank 들로 이루어진 list를 리턴합니다.
    """
    relative_ranks = []
    
    for match in matchlist:
        
        # 간혹 matchRank가 공란인 경우가 있음
        if (match.playerCount in n_players) and (match.player.matchRank in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '99']):

            rank = int(match.player.matchRank) # rank 정보 추출
        
            if rank == 99: # 리타이어는 99등으로 집계
                if include_retire == True: # include_retire가 True인 경우 최저 상대순위(1) 를 부여하고, False인 경우 무시함
                    relative_ranks.append(1)
            else:
                relative_ranks.append(round(rank / match.playerCount, 3))
    
    return relative_ranks

def get_channelNames(matchlist, ascending = False) -> dict:
    """
    matchlist를 받아, 해당 list에서 경기 타입 정보를 추출하여 dict 형태로 리턴합니다.
    ascending 변수를 통해 경기 횟수에 대해 ascending, descending order 설정이 가능합니다.

    Args:
        matchlist : matchlist (list): Match() 객체로 이루어진 list입니다. get_matchlist의 리턴형과 동일합니다.
        ascending (bool, optional): 경기 횟수가 많은 순서대로 나열하는지의 여부입니다. False인 경우 내림차순으로 정렬됩니다. default = False

    Returns:
        dict: {channelname : 경기 횟수, ... } 형태의 dictionary를 리턴합니다.
    """
    
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
    
    if ascending == False:
        modecount = sorted(modecount.items(), key = lambda item: item[1], reverse = True)
    else:
        modecount = sorted(modecount.items(), key = lambda item: item[1], reverse = False)
        
    modecount = dict(modecount)
    
    return modecount

def bar_ranks(ranks : list, name : str, n_players = 8) -> None:
    """rank 정보를 입력받은 후, 해당 정보를 토대로 막대그래프를 생성합니다.

    Args:
        ranks (list): rank로 이루어진 list를 의미합니다.
        name (str): 플레이어의 이름을 의미합니다.
        n_players (int, optional): 총 플레이어의 수 (x축의 범위)를 의미합니다. Defaults to 8.
    """
    
    try:
        ranks = list(map(int, ranks)) # 정수로 형변환되지 않는 input에 대해 예외를 발생합니다.
    except:
        print('invalid input')
    
    # 제목 한글 표시 관련 설정
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    
    X = np.arange(1, 9)
    y = [0 for i in range(n_players)]
    
    for rank in ranks:
        y[rank - 1] += 1
        
    plt.bar(X, y, align='center', edgecolor='lightgray', linewidth=5)
    plt.title(name)
    plt.show()
        
################### test code #####################

if __name__ == '__main__':
    
    #### test of get_user ####
    user = get_user_by_nickName('MOOOMOO')
    user_info = get_user_by_accountNo(user.accountNo)
    
    print(user_info.level) # 108
    
    accountNo = user.accountNo
    
    #### test of get_matchlist ####
    
    matchlist = get_matchlist(
        accountNo = accountNo, startTime = '', endTime = '', # startTime, endTime을 따로 지정하지 않는 경우, 자동으로 최근 500건의 매치를 받아옵니다.
        matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', # matchType : 스피드 개인전
        limit = 10
        )
    
    # for match in matchlist:
    #     print(match.matchId)
        
    #### test of get_matchInfo ####
    
    test_matchId = matchlist[0].matchId
    matchInfo = get_matchInfo(test_matchId)
    print(matchInfo['channelName'])
    
    #### test of get_ranks, bar_ranks ####
    
    ranks = get_ranks(matchlist, n_players=[8])
    print(ranks)
    
    bar_ranks(ranks, 'MOOOMOO', 8)