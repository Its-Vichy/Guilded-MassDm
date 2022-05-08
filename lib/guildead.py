# Lasted wrapper version: https://github.com/Its-Vichy/Guildead

import requests, uuid, random, string

class Exploit:
    def blank_message():
        return [random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) for _ in range(random.randint(1000, 1000))]

class Guilded:
    def __init__(self, proxy: str= None):
        self.base_url = "https://www.guilded.gg/api"
        self.session = requests.Session()
        self.session.proxies = {"http": proxy, "https": proxy} if proxy else None

        self.ratelimit = None

        self.user = {}
        self.profil = {}

    def login(self, email: str, password: str):
        r = self.session.post(f'{self.base_url}/login', json={'email': email, 'password': password, 'getMe': True})

        if 'Email or password is incorrect.' in r.text:
            return (False, {'error': 'Email or password is incorrect.'})
        elif 'You have been banned.' in r.text:
            return (False, {'error': 'You have been banned.'})
        else:
            try:
                self.user = r.json()['user']
                self.profil = r.json()
            except:
                pass

            return (True, {'mid': r.cookies.get('guilded_mid'), 'hmac_signed_session': r.cookies.get('hmac_signed_session')})

    def login_from_token(self, token: str, get_me: bool= False):
        self.session.cookies.set('hmac_signed_session', token)

        if get_me:
            self.get_me()
    
    def get_me(self):
        resp = self.session.get(f'{self.base_url}/me?isLogin=false&v2=true').json()
        self.user = resp['user']

        return resp

    def send_message(self, channel_id: str, message: str, confirmed: bool= False, isSilent: bool= False, isPrivate: bool= False, repliesTo: list= []):
        r = self.session.post(f'{self.base_url}/channels/{channel_id}/messages', json={
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
        r = self.session.put(f'{self.base_url}/channels/{channel_id}/messages/{message_id}', json={
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
        r = self.session.delete(f'{self.base_url}/channels/{channel_id}/messages/{message_id}')
        return r.json()
    
    def join_server(self, invite_code: str):
        r = self.session.put(f'{self.base_url}/invites/{invite_code}')
        return r
    
    def add_friend(self, ids: list):
        r = self.session.post(f'{self.base_url}/users/me/friendrequests', json={"friendUserIds": ids})
        return r.json()
    
    def check_mail_verified(self):
        r = self.session.get(f'{self.base_url}/users/me/verification')
        return r.json()
    
    def get_server_info(self, invite_code: str):
        r = self.session.get(f'{self.base_url}/content/route/metadata?route=%2F{invite_code}')
        return r.json()

    def join_team(self, team_id: str):
        user_id = self.user['id']
        
        r = self.session.put(f'{self.base_url}/teams/{team_id}/members/{user_id}/join', json={'inviteId': None})
        return r

    def set_activity(self, number: int = 1):
        # online, idle, dnd

        r = self.session.post(f'{self.base_url}/users/me/presence', json={'status': number})
        return r.json()
    
    def ping(self):
        r = self.session.put(f'{self.base_url}/users/me/ping', json={})
        return r.json()
    
    def set_status(self, text: str, customReactionId: int = 90002573):
        r = self.session.post(f'{self.base_url}/users/me/status', json={
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
        return r.json()
    
    def set_bio(self, text: str):
        user_id = self.user['id']

        r = self.session.put(f'{self.base_url}/users/{user_id}/profilev2', json={"userId": user_id,"aboutInfo":{"tagLine": text}})
        return r.json()

    def add_pfp(self, url):
        #url = self.session.post('https://media.guilded.gg/media/upload?dynamicMediaTypeId=UserAvatar', files={'file': open(image_path, 'rb')}, headers={'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary20al5Fdtd69OqIRT'}).json()
        
        return self.session.post(f'{self.base_url}/users/me/profile/images', json={'imageUrl': url})

    def get_guild_member(self, guild_id: str):
        return self.session.get(f'{self.base_url}/teams/{guild_id}/members')

    #def get_guild_member_detail(self, guild_id: str):
    #    return self.session.get(f'{self.base_url}/teams/{guild_id}/members/detail')
    
    def open_dm_channel(self, user_id: str):
        return self.session.post(f'{self.base_url}/users/{self.user["id"]}/channels', json={"users":[{"id": user_id}]})