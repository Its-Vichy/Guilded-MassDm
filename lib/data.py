class Data:
    def __init__(self):
        self.cookies = list(set(open('./data/cookies.txt', 'r+').read().splitlines()))