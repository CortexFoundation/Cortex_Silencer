from flask import Flask,request
from flask import request
from Crypto.Hash import SHA256
from Block import Blockchain
import os
import json
import time
import threading
def cmp(a,b):
        return a["nonce"]-b["nonce"]
class Node:
    def __init__(self):
        self.node = Flask(__name__)
        #store unpacked trascations
        self.unpacked_trasactions = []
        self.memory_pool = []
        self.blockchain = Blockchain()
        self.lock = threading.Lock()
        self.miner_address = "0x0000000000000000000000000000000000000000001"


        @self.node.route('/txion', methods=['POST'])
        def transaction():
            self.lock.acquire()
            if request.method == 'POST':
                # On each new POST request,
                # we extract the transaction data
                new_txion = request.get_json()
                if not new_txion:
                    new_txion = json.load(request.files["json"])
                assert("nonce" in new_txion.keys())
                assert("from" in new_txion.keys())
                # print new_txion
                # Then we add the transaction to our list
                # Because the transaction was successfully
                # submitted, we log it to our console
                info = {}
                contractType = new_txion["type"]
                info["tx_hash"] = SHA256.new(data=(str(int(time.time()*1000))).encode()).hexdigest()
                if contractType == "tx":
                    assert("to" in new_txion.keys())
                    assert("amount" in new_txion.keys())
                elif contractType == "model_data":
                    assert("filename" in new_txion.keys())
                    f = request.files["file"]
                    p = os.path.join("model",new_txion["filename"])
                    model_addr = SHA256.new(data=(str(int(time.time()*1000))).encode()).hexdigest()
                    f.save(p)
                    new_txion["model_addr"] = model_addr
                    new_txion["model_path"] = p
                    info["model_addr"] = model_addr
                elif contractType == "param_data":
                    assert("filename" in new_txion.keys())
                    f = request.files["file"]
                    p = os.path.join("param",new_txion["filename"])
                    param_addr = SHA256.new(data=(str(int(time.time()*1000))).encode()).hexdigest()
                    f.save(p)
                    new_txion["param_addr"] = param_addr
                    new_txion["param_path"] = p
                    info["param_addr"] = param_addr
                elif contractType == "input_data":
                    assert("filename" in new_txion.keys())
                    f = request.files["file"]
                    p = os.path.join("input_data",new_txion["filename"])
                    input_addr = SHA256.new(data=(str(int(time.time()*1000))).encode()).hexdigest()
                    f.save(p)
                    new_txion["input_addr"] = input_addr
                    new_txion["input_path"] = p
                    info["input_addr"] = input_addr
                elif contractType == "contract_call":
                    assert("input_address" in new_txion.keys())
                    assert("contract_address" in new_txion.keys())
                elif contractType == "contract_create":
                    assert("model_address" in new_txion.keys())
                    assert("param_address" in new_txion.keys())
                    contract_addr = SHA256.new(data=(str(int(time.time()*1000))).encode()).hexdigest()
                    new_txion["contract_addr"] = contract_addr
                    info["contract_addr"] = contract_addr
                else:
                    self.lock.release()
                    return json.dumps({"msg":"error, no such type"})
                # except Exception as ex:
                    # return json.dumps({"msg":"error "+str(ex)})
                self.memory_pool.append(new_txion)
                self.lock.release()
                return json.dumps({"msg":"ok","info":info})
            self.lock.release()
        @self.node.route('/mine', methods=['POST'])
        def mine():
            self.lock.acquire()
            # if len(self.unpacked_trasactions)==0:
                # self.lock.release()
                # return json.dumps({"msg":"error, there is no unpacked transaction"})
            self.unpacked_trasactions = sorted(self.memory_pool[:],cmp=cmp)
            block_hash,err = self.blockchain.pack(self.unpacked_trasactions, self.miner_address)
            if not err:
                self.memory_pool = self.memory_pool[len(self.unpacked_trasactions):]
                self.lock.release()
                return json.dumps({"msg":"ok"})
            else:
                self.lock.release()
                return json.dumps({"msg":"error, %s"%err})
        @self.node.route('/getStates',methods=['GET'])
        def getStates():
            self.lock.acquire()
            s = json.dumps(self.blockchain.CVM.state)
            self.lock.release()
            return s
        @self.node.route('/getBlock',methods=['GET'])
        def getBlock():
            self.lock.acquire()
            s = json.dumps([i.getDict() for i in self.blockchain._chain])
            self.lock.release()
            return s
if __name__ == "__main__":
    Node().node.run()
