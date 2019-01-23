import hashlib
import time

blocks = []


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def isValidhash(hash):
    if hash.startswith("0000"):
        return True
    return False


def hashBlock(data, timestamp, previoushash, index):
    _hash = ""
    nonce = 0
    while not isValidhash(_hash):
        _input = data + str(timestamp) + str(previoushash) + str(index) + str(nonce)
        _hash = encrypt_string(_input)
        nonce += 1
        print(nonce)
    blocks.append(_hash)


def getLastHash():
    return blocks[len(blocks) - 1]


def addNewBlock(mmessage):
    _index = len(blocks)
    timestamp = time.time()
    previousHash = getLastHash()
    hashBlock(mmessage, timestamp, previousHash, _index)


def getAllBlocks():
    for i in range(0, len(blocks)):
        print(blocks[i])


def initBlock():
    data = "hello world"
    timestamp = time.time()
    previoushash = 0
    index = 0
    hashBlock(data, timestamp, previoushash, index)