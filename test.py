import requests
import json
import matplotlib.pyplot as plt

from data import Data

import utils

matchlist = utils.get_matchlist(accountNo='973305538', startTime='2010-09-04T08:40:24', endTime='2022-03-04T08:40:24',
    matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a')

'''
{
    'channelName': 'speedIndiCombine', 
    'startTime': '2022-09-04T08:40:24.744000', 
    'endTime': '2022-09-04T08:42:07.634000', 
    'gameSpeed': 7, 
    'matchId': '0339000be9fc8591', 
    'matchResult': '0', 
    'matchType': '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a', 
    'playTime': 91, 
    'trackId': '3c03b354c083aa8311b62221f535b6228f935e9b3a9352b0f2c1c71ac7833544', 
    'players': [
        {
            'accountNo': '319356569', 
            'characterName': 'Limebox1022', 
            'character': 'ebc1215d5c702d47985836ab63710eb7b6bec34af0735f1afa277cb426d663fb', 
            'kart': 'dd0685efa8397ab65468ea28f229fa61a1ca2e8fe7e311bcb3650d14509771b4', 
            'license': '', 
            'pet': '0623ce0b5f3b797eed2e009ce02ed81df11f375a3dfdfe1962f0260cb9770f79', 
            'flyingPet': '13e247466d75204e1b3d587abcc11def087f6ffcdfcf798cb2c4b8edcddd8f5b', 
            'partsEngine': '0', 
            'partsHandle': '0', 
            'partsWheel': '0', 
            'partsKit': '0', 
            'rankinggrade2': '0', 
            'matchRank': '99', 
            'matchRetired': '1', 
            'matchWin': '0', 
            'matchTime': ''
            }, 
        {
            'accountNo': '1073938567', 
            'characterName': '0LJ천상의LJ0', 
            'character': '42c729e64e31aea803e4881432f7b95129ce97535c29e4f9a72919a9f267b418', 
            'kart': 'd47aa62de79d88ecee263e07456555d99ff8957f1760d0f248667913acbc2b67', 
            'license': '', 
            'pet': '492e06ae60ff9d70c311cab587117173484ff667a58832d76f72c46497b63139', 
            'flyingPet': '13e247466d75204e1b3d587abcc11def087f6ffcdfcf798cb2c4b8edcddd8f5b', 
            'partsEngine': '1', 
            'partsHandle': '1', 
            'partsWheel': '1', 
            'partsKit': '1', 
            'rankinggrade2': '3', 
            'matchRank': '4', 
            'matchRetired': '0', 
            'matchWin': '0', 
            'matchTime': '87167'
            }
        ]
    }
'''

nicknames = ['갓트라넥', 'MysTic벤츠', 'MOOOMOO', 'TwitchTV', 'MusicTherapy', '개뛰는일영', '폴창', '에퍼한상현']
accountNos = []

for nickname in nicknames:
    userinfo = utils.get_user_by_nickName(nickname) # nickname을 통해 utils.User 인스턴스 형태의 유저 정보를 가져옵니다
    accountNos.append(userinfo.accountNo) # 각 User에서 accessId를 추출합니다.
    
# all_matchlists : list[list], 모든 플레이어들의 matchlist를 저장
all_matchlists : list = []

for accountNo in accountNos:
    matchlist = utils.get_matchlist(
        accountNo = accountNo, startTime = '', endTime = '', # startTime, endTime을 따로 지정하지 않는 경우, 자동으로 최근 500건의 매치를 받아옵니다.
        matchType='7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a' # matchType : 스피드 개인전으로 한정
        )
    all_matchlists.append(matchlist) # 각 플레이어의 matchlist를 all_matchlists에 추가합니다.

print(len(all_matchlists))

for match in all_matchlists[0]:
    print(match.player.matchRank + 'end')


# relative_ranks : list = utils.get_relative_ranks(matchlist, n_players = [5, 6, 7, 8], include_retire=False)
