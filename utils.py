import requests
import json

key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6Ijk3MzMwNTUzOCIsImF1dGhfaWQiOiIyIiwiZXhwIjoxNjgzMTkwNDYyLCJpYXQiOjE2Njc2Mzg0NjIsIm5iZiI6MTY2NzYzODQ2Miwic2VydmljZV9pZCI6IjQzMDAxMTM5MyIsInRva2VuX3R5cGUiOiJBY2Nlc3NUb2tlbiJ9.o4oNGosgyTmNuSt752GBIFQMozxKYkPLDkfGEKEEBMk'

def get_user_by_nickname(nickname, key = key):
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickname}',
        headers=headers
    )
    return response.json()

def get_user_by_access_id(access_id, key = key):
    """get user nickname by access id

    Args:
        access_id (int, string): _description_
        key (access key, optional): _description_. Defaults to key.

    Returns:
        response in json type
    """
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{access_id}',
        headers=headers
    )
    return response.json()

# continue...
def get_matchlist(access_id, start_date, end_date, offset, limit, match_types):
    headers = {'Authorization' : key}
    response = requests.get(
        f'https://api.nexon.co.kr/kart/v1.0/users/{access_id}/matches?start_date={start_date}&end_date={end_date}&offset={offset}&limit={limit}&match_types={match_types}',
        headers=headers
    )
    return response.json()  

# 기본기능 : 일정 기간의 순위 변동 그래프 (start_time, end_time, match_types)
def return_ranks(access_id : str, start_date : str, end_date : str, match_types : str):
    ranks = []
    json = get_matchlist(access_id, start_date, end_date, offset = 0, limit = 2, match_types = match_types)

    print(json)

    for match in range(json):
        ranks.append(match['player']['matchRank'])
    return ranks

################### test code #####################

if __name__ == '__main__':
    return_ranks('973305588', '2021-09-04T08:40:24', '2022-09-04T08:40:24', '7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a')