import json
from collections import defaultdict
class CVM:
    def __init__(self):
        self.state = {
            "account":defaultdict(lambda: 0),
            #address:file_path
            "model_address":defaultdict(lambda:None),
            "param_address":defaultdict(lambda:None),
            "contract_address":defaultdict(lambda:None),
            "result":defaultdict(lambda:None),
            "last_nonce":defaultdict(lambda:-1)
        }
    def verify(self,unpacked_transactions):
        self.new_state = self.state.copy()
        account = self.new_state["account"]
        model_address = self.new_state["model_address"]
        param_address = self.new_state["param_address"]
        contract_address = self.new_state["contract_address"]
        result = self.new_state["result"]
        last_nonce = self.new_state["last_nonce"]
        for t in unpacked_transactions:
            if t["type"] == "tx":
                if account[t["from"]]<int(t["amount"]):
                    return None,"transaction %s is invalid, not enough cortex"%t["tx_hash"]
                if int(t["amount"])<0:
                    return None, "transaction %s is invalid, amount need to be not negative"%t["tx_hash"]
                if int(t["nonce"])<=last_nonce[t["from"]]:
                    return None, "transaction %s is invalid, nonce should be ascending "%t["tx_hash"]
                account[t["from"]]-=int(t["amount"])
                account[t["to"]]+=int(t["amount"])
            if t["type"] == "model_data":
                model_address[t["model_addr"]] = t["model_path"]
            if t["type"] == "param_data":
                param_address[t["param_addr"]] = t["param_path"]
            if t["type"] == "input_addr":
                param_address[t["param_addr"]] = t["param_path"]
            if t["type"] == "coinbase_tx":
                account[t["miner_addr"]]+=100
            if t["type"] == "contract_create":
                contract_address[t["contract_addr"]] = {
                    "model_address":t["model_address"],
                    "param_address":t["param_address"]
                }
            if t["type"] == "contract_call":
                result[t["from"]] = t["contract_address"]+t["input_address"]
        return self.new_state,None
