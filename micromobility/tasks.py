from celery import app
from django.utils import timezone
from dataclasses import dataclass
from .tools import RedisServer, ethTestnet, Timer_settings
from .models import Auction



@app.shared_task
def auction_end(auction_pk):
    redis = RedisServer()
    winner = redis.read(key=auction_pk)
    model = Auction.objects.filter(pk=auction_pk)[0]
    eth = ethTestnet(model.dataSerializer())
    if winner == None:
        model.update(status="closed")
        return "no winner"
    else:
        model.update(
            winner=winner["user"],
            finalPrice=winner["bid"],
            status="closed",
            end=timezone.now(),
            ethTx="PENDING",
        )
        try:        
            tx = eth.saveOnChain()
            model.update(ethTx=tx)
        except:
            check_after_error = eth.checkTransaction()
            if check_after_error == 'Failure with the on chain save':
                retry = eth.saveOnChain()
                model.update(ethTx=retry)
            else:

                model.update(ethTx=check_after_error)
        RedisServer.delete(auction_pk)
        return True


def schedule_auction_end(auction):
    end_time = auction.start + Timer_settings.time
    auction_end.apply_async(args=[auction.pk], eta=end_time)
