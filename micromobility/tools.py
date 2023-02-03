from dataclasses import dataclass, field
import redis as redis
from random import randint
import json
from django.core.exceptions import PermissionDenied
from django.utils import timezone as tz
from web3 import Web3
from .secret import PKEY, ADDRESS, ROPSTEN
from django.utils import timezone

def check_permission(view):
    """decorator to make sure the user is viewing his items and denied entry on other items"""
    def check(request, username):
        if request.user.username == username:
            return view(request, username)
        else:
            raise PermissionDenied()
    return check

@dataclass
class Timer_settings:
    time: timezone = timezone.timedelta(seconds=120)

class RedisServer:

    def __init__(self, port=6380, host='localhost'):
        try:
            self.redis = redis.Redis(host=host, port=port, db=0, decode_responses=True)
        except:
            raise ConnectionError

 
    def write(self, auctionId, user, bid):
        data: dict = dict(user=user, bid=bid, date=tz.now().strftime("%m/%d/%Y, %H:%M:%S"))        
        return self.redis.set(auctionId, json.dumps(data))


    def read(self, key):
        content = self.redis.get(key)
        if content == None:
            return None
        else:
            return json.loads(content)
    
    @classmethod
    def get_last_proposal(cls, key):
        server = cls(port=6380, host='localhost')
        value = server.read(key)
        return value
    
    @classmethod
    def delete(cls, key):
        server = cls(port=6380, host='localhost')
        try:
            server.delete(key)
            return True
        except:
            return False
            
class ethTestnet():

    def __init__(self, values):
        self.values = values
        self.txId = ""

    def checkTransaction(self):
        WEB3 = Web3(Web3.HTTPProvider(ROPSTEN))
        try:
            txHash = WEB3.eth.waitForTransactionReceipt(self.txId, timeout=120, poll_latency=0.1)
            return txHash['transactionHash'].hex()
        except:
            return 'Failure with the on chain save'

    def saveOnChain(self):
        WEB3 = Web3(Web3.HTTPProvider(ROPSTEN))
        nonce = WEB3.eth.getTransactionCount(ADDRESS)
        gasPrice = WEB3.eth.gasPrice
        value = WEB3.toWei(0, 'ether')
        signedTx = WEB3.eth.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=gasPrice,
            gas=100000,
            to='0x0000000000000000000000000000000000000000',
            value=value,
            data=self.values.encode('utf-8')), PKEY)
        tx = WEB3.eth.sendRawTransaction(signedTx.rawTransaction)
        self.txId = WEB3.toHex(tx)
        return self.txId
    

  
        

    
    
