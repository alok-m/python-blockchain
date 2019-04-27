import json
import requests
from _sha256 import sha256
from time import time
from typing import Optional
from urllib.parse import urlparse


FORGE_TRIGGER = 1

class Blockchain:
    def __init__(self):
        self.authority = []
        self.blocs = []
        self.peers = set()
        self.mempool = []

        self.forge(prev_hash='genesis', curr_hash=None)

    def forge(self, prev_hash: Optional[str], curr_hash: Optional[str]):
        # noinspection PyDictCreation
        bloc = {
            'previous_hash': prev_hash or self.previous_block['current_hash'],
            'current_hash': '',
            'timestamp': int(time()),
            'transactions': self.mempool[:FORGE_TRIGGER]
        }
        bloc['current_hash'] = curr_hash or self.hash(bloc)
        self.blocs.append(bloc)

    def new_transaction(self, sender: str, content: dict):
        if(sender in self.peers):
            self.mempool.append({
                'sender': sender,
                'content': content
            })

    def mine(self, miner: str) -> int:
        mempool_size = len(self.mempool)
        print(mempool_size)
        if mempool_size < FORGE_TRIGGER:
            return 1
        elif mempool_size == FORGE_TRIGGER:
            self.forge(prev_hash=None, curr_hash=None)
            self.mempool = self.mempool[FORGE_TRIGGER:]
            return 0
        elif(mempool_size > FORGE_TRIGGER):
            while(len(self.mempool) >= FORGE_TRIGGER):
                self.forge(prev_hash=None, curr_hash=None)
                self.mempool = self.mempool[FORGE_TRIGGER:]
            return 0
        
    def register(self, address: str):
        parsed_url = urlparse(address)
        self.peers.add(parsed_url.path)

    def sync(self) -> bool:
        changed = False
        for peer in self.peers:
            r = requests.get(f'http://{peer}/')

            if r.status_code != 200:
                continue

            chain = r.json()['chain']
            if len(chain) > len(self.blocs):
                self.blocs = chain
                changed = True

        return changed

    @property
    def previous_block(self) -> dict:
        return self.blocs[-1]

    @staticmethod
    def hash(block: dict):
        to_hash = json.dumps(block)
        return sha256(to_hash.encode()).hexdigest()

    def set_authority(self, address: str):
        self.authority.append(address)
