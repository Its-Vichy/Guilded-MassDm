from lib.guildead import Guilded

class Scrapper:
    def __init__(self, scrape_token: str):
        self.scrape_token = scrape_token
        self.api = Guilded()

        self.api.login_from_token(self.scrape_token)
    
    def scrape_avatar(self, guild_id: str):
        members = self.api.get_guild_member(guild_id)['members']
        avatars = []

        for member in members:
            try:
                avatars.append(member['profilePicture'])
            except:
                pass

        return avatars
    
    def scrape_username(self, guild_id: str):
        members = self.api.get_guild_member(guild_id)['members']
        usernames = []

        for member in members:
            usernames.append(member['name'])
        
        return usernames

    def scrape_members_ids(self, guild_id: str):
        members = self.api.get_guild_member(guild_id)['members']
        ids = []

        for member in members:
            if 'type' not in str(member):
                ids.append(member['id'])
        
        return ids