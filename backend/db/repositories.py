import asyncpg

class Repositories:

    def __init__(self, db: asyncpg.Connection):
        self.db = db

    
        