# Lasted wrapper version: https://github.com/Its-Vichy/Guildead

import requests, uuid, random, string, itertools

from requests.models import Response

class Exploit:
    def blank_message():
        return [random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) for _ in range(random.randint(1000, 1000))]

class Guilded:
    def __init__(self, proxy: itertools.cycle):
        self.base_url = "https://www.guilded.gg/api"
        self.session = requests.Session()
        self.proxy = proxy

        self.ratelimit = None

        self.user_id = ''
        self.user = {}
        self.profil = {}
    
    def post(self, path: str, json: dict):
        while True:
            p = 'http://' + next(self.proxy)
            self.session.proxies = {"http": p, "https": p} if self.proxy else None

            try:
                return self.session.post(path, json=json)
            except Exception as e:
                continue
        
    def put(self, path: str, json: dict=None):
        while True:
            p = 'http://' + next(self.proxy)
            self.session.proxies = {"http": p, "https": p} if self.proxy else None

            try:
                return self.session.put(path, json=json)
            except Exception as e:
                continue
    
    def delete(self, path: str):
        while True:
            p = 'http://' + next(self.proxy)
            self.session.proxies = {"http": p, "https": p} if self.proxy else None

            try:
                return self.session.delete(path)
            except Exception as e:
                continue
    
    def get(self, path: str):
        while True:
            p = 'http://' + next(self.proxy)
            self.session.proxies = {"http": p, "https": p} if self.proxy else None

            try:
                return self.session.get(path)
            except Exception as e:
                continue

    def login(self, email: str, password: str):
        r = self.post(f'{self.base_url}/login', json={'email': email, 'password': password, 'getMe': True})

        if 'Email or password is incorrect.' in r.text:
            return (False, {'error': 'Email or password is incorrect.'})
        elif 'You have been banned.' in r.text:
            return (False, {'error': 'You have been banned.'})
        else:
            try:
                self.user = r.json()['user']
                self.profil = r.json()
                self.user_id = self.user['id']
            except:
                pass

            return (True, {'mid': r.cookies.get('guilded_mid'), 'hmac_signed_session': r.cookies.get('hmac_signed_session')})

    def login_from_token(self, token: str, get_me: bool= False):
        self.session.cookies.set('hmac_signed_session', token)

        if get_me:
            self.get_me()
    
    def get_me(self):
        resp = self.get(f'{self.base_url}/me?isLogin=false&v2=true').json()
        self.user = resp['user']
        self.user_id = self.user['id']

        return resp

    def send_message(self, channel_id: str, message: str, confirmed: bool= False, isSilent: bool= False, isPrivate: bool= False, repliesTo: list= []):
        r = self.post(f'{self.base_url}/channels/{channel_id}/messages', json={
            "messageId": str(uuid.uuid1()),
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": message,
                                            "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "repliesToIds": repliesTo,
            "confirmed": confirmed,
            "isSilent": isSilent,
            "isPrivate": isPrivate
        })
        return r
    
    def edit_message(self, channel_id: str, message_id: str, message: str, confirmed: bool= False, isSilent: bool= False, isPrivate: bool= False, repliesTo: list= []):
        r = self.put(f'{self.base_url}/channels/{channel_id}/messages/{message_id}', json={
            "messageId": message_id,
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": message,
                                            "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "repliesToIds": repliesTo,
            "confirmed": confirmed,
            "isSilent": isSilent,
            "isPrivate": isPrivate
        })
        return r.json()
    
    def delete_message(self, channel_id: str, message_id: str):
        return self.delete(f'{self.base_url}/channels/{channel_id}/messages/{message_id}').json()
    
    def join_server(self, invite_code: str):
        r = self.put(f'{self.base_url}/invites/{invite_code}')
        return r
    
    def add_friend(self, ids: list):
        r = self.post(f'{self.base_url}/users/me/friendrequests', json={"friendUserIds": ids})
        return r.json()
    
    def check_mail_verified(self):
        r = self.get(f'{self.base_url}/users/me/verification')
        return r.json()
    
    def get_server_info(self, invite_code: str):
        r = self.get(f'{self.base_url}/content/route/metadata?route=%2F{invite_code}')
        return r.json()

    def join_team(self, team_id: str):
        user_id = self.user_id
        
        r = self.put(f'{self.base_url}/teams/{team_id}/members/{user_id}/join', json={'inviteId': None})
        return r

    def set_activity(self, number: int = 1):
        # online, idle, dnd

        r = self.post(f'{self.base_url}/users/me/presence', json={'status': number})
        return r
    
    def ping(self):
        r = self.put(f'{self.base_url}/users/me/ping', json={})
        return r
    
    def set_status(self, text: str, customReactionId: int = 90002573):
        r = self.post(f'{self.base_url}/users/me/status', json={
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": text,
                                            "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "customReactionId": customReactionId,
            "expireInMs": 0
        })
        return r
    
    def set_bio(self, text: str):
        user_id = self.user_id

        r = self.put(f'{self.base_url}/users/{user_id}/profilev2', json={"userId": user_id,"aboutInfo":{"tagLine": text}})
        return r

    def add_pfp(self, url):
        #url = self.session.post('https://media.guilded.gg/media/upload?dynamicMediaTypeId=UserAvatar', files={'file': open(image_path, 'rb')}, headers={'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary20al5Fdtd69OqIRT'}).json()
        
        return self.session.post(f'{self.base_url}/users/me/profile/images', json={'imageUrl': url})

    def get_guild_member(self, guild_id: str):
        return self.get(f'{self.base_url}/teams/{guild_id}/members')
    
    def open_dm_channel(self, user_id: str):
        return self.session.post(f'{self.base_url}/users/{self.user_id}/channels', json={"users":[{"id": user_id}]})

    def get_servers(self, limit: int=10):
        return self.session.post(f'{self.base_url}/explore/teams', json={"filters":{},"limit":limit,"sections":["allTeams"],"offset":{"createdAt":"2022-05-20T01:11:58.827Z"}})

    def leave_server(self, guild_id: str, member_id: str):
        return self.delete(f'{self.base_url}/teams/{guild_id}/members/{member_id}')