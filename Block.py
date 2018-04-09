import hashlib as hasher
from Crypto.Hash import SHA256
import datetime as date
from CVM import CVM
import time
import json
from collections import defaultdict
class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.hash_block()

    def hash_block(self):
        sha = SHA256.new((str(self.index) +
        str(self.timestamp) +
        str(self.data) +
        str(self.previous_hash) +
        str(self.nonce)).encode())
        return sha.hexdigest()
    def getDict(self):
        return {
            "index":self.index,
            "previous_hash":self.previous_hash,
            "timestamp":int(self.timestamp),
            "data":self.data,
            "nonce":self.nonce,
            "hash":self.hash
        }

class Blockchain(object):
    def __init__(self):
        self._chain = [self.create_genesis_block()]
        self._chain_name = defaultdict(lambda:[])
        self.CVM = CVM()
    # ...blockchain
    def create_genesis_block(self):
        # Manually construct a block with
        # index zero and arbitrary previous hash
        return Block(
                index =0,
                timestamp = int(time.time()*1000),
                data = [],
                previous_hash = "0",
                nonce = 0)
    def add_block(self,data):
        last_block = self._chain[-1]
        new_index = self._chain[-1].index+1
        new_timestamp = int(time.time()*1000)
        previous_hash = last_block.hash
        header = str(new_index) + str(new_timestamp) + str(data) + str(previous_hash)
        hash_result,nonce = self.proof_of_work(header)
        b = Block(
                index = new_index,
                timestamp = new_timestamp,
                data = data,
                previous_hash = previous_hash,
                nonce = nonce)
        self._chain.append(b)
        visit = defaultdict(lambda:False)
        for t in data:
            if "from" in t.keys() and not visit[t["from"]]:
                self._chain_name[t["from"]].append(b)
                visit[t["from"]] = True
            if "to" in t.keys() and not visit[t["to"]]:
                self._chain_name[t["to"]].append(b)
                visit[t["to"]] = True
        return self._chain[-1]
    def pack(self,unpaced_transactions, miner_address):
        temp_tx = [i for i in unpaced_transactions]
        temp_tx.append({"type":"coinbase_tx","miner_addr":miner_address,"reward":5})
        new_state, err = self.CVM.verify(temp_tx)
        if err:
            return None,err
        return self.add_block(temp_tx),None

    def proof_of_work(self,header):
        target = 2**250
        nonce = 0
        while True:
            hash_result = SHA256.new(data=(str(header)+str(nonce)).encode()).hexdigest()
            if int(hash_result,16)<target:
                return hash_result, nonce
            nonce+=1
