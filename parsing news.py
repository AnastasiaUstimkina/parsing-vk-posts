import requests
import json

access_token = ''

def write_json(data):
    with open('news.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=5, ensure_ascii=False)
       
        
def create_uri(method: str, query_params: dict) -> str:
    params_string = '&'.join(
        [f'{key}={value}' for (key, value) in query_params.items()]
    )
    return f'https://api.vk.com/method/{method}?access_token={access_token}&v=5.52&{params_string}'


def make_request(method: str, query_params: dict) -> dict:
    uri = create_uri(method, query_params)
    response_dict = requests.get(uri).json()
    return response_dict

        
def get_posts(group_id, count):
    response = make_request('wall.get', {'owner_id': group_id, 'count': count, 'offset': 0})
    write_json(response)
    return response
    
    
group_id = '-15755094'
count = 100

posts = get_posts(group_id, count)


def get_items(posts):
    items = {}
    user_activity = {}
    for post in posts['response']['items']:
        items[post['id']] = {'date': post['date'], 'text': post['text']}
        
        user_activity[post['id']] = {'comments':{'count': post['comments']['count'], 'text': ''}, 
                                     'likes': post['likes']['count'], 'reposts': post['reposts']['count']}

items = get_items(posts)
        