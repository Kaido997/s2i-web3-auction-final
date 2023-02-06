from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
from .tools import RedisServer
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .tools import Timer_settings
from django.utils import timezone


def get_sentinel_user():
    deluser = get_user_model().objects.get_or_create(username="deleted")[0]
    return Profile.create(user=deluser)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchList = models.JSONField(default=json.dumps(list()))

    @classmethod
    def create(cls, user: User):
        return cls(user=user).save()

    def add_delete_from_watchList(self, auctionId, delete=False):
        if delete == False:
            if Auction.objects.get(pk=auctionId).status == "o":
                _list = list(json.loads(self.watchList))
                if auctionId in _list:
                    return False
                else:
                    _list.append(auctionId)
                    self.watchList = json.dumps(_list)
                    self.save()
                    return True
            else:
                return False
        else:
            decodedL: list = json.loads(self.watchList)
            try:
                decodedL.remove(auctionId)
                self.watchList = json.dumps(decodedL)
                self.save()
                return True
            except:
                return False

    def __str__(self) -> str:
        return str(self.user.username)


def currentpk():
    try:
        latest = Auction.objects.latest("pk").pk
        return latest + 1
    except:
        return 0


class Auction(models.Model):
    STATUS = (
        ("c", "CLOSE"),
        ("o", "OPEN"),
    )
    VEHICLES = (
        ("powered standing scooter", "powered_standing_scooter"),
        ("powered bicycle", "powered_bicycle"),
        ("powered seated_scooter", "powered_seated_scooter"),
        ("powered self-balacing_board", "powered_self-balacing_board"),
        ("powered non-self-balancing_board", "powered_non-self-balancing_board"),
        ("powered skates", "powered_Skates"),
    )
    auctionId = models.PositiveIntegerField(default=0)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(
        Profile, on_delete=models.SET(get_sentinel_user), blank=True, null=True
    )
    initPrice = models.PositiveIntegerField(default=None, blank=True)
    finalPrice = models.PositiveIntegerField(default=None, blank=True, null=True)
    ethTx = models.CharField(max_length=256, blank=True)
    item = models.CharField(choices=VEHICLES, max_length=32, default=None)
    status = models.CharField(choices=STATUS, max_length=32, default="o")

    @classmethod
    def create(cls, auctionId, item, initPrice):
        return cls(auctionId=auctionId, item=item, initPrice=initPrice).save()

    def get_last_bid(self):
        try:
            result = RedisServer.get_last_proposal(self.pk)
            return result["bid"]
        except:
            return 0

    def update(self, *args, **kwargs):
        for arg in kwargs:
            if arg == "winner":
                self.winner = Profile.objects.get(
                    user=User.objects.get(username=kwargs[arg])
                )
            elif arg == "finalPrice":
                self.finalPrice = kwargs[arg]
            elif arg == "status":
                self.status = kwargs[arg]
            elif arg == "ethTx":
                self.ethTx = kwargs[arg]
            elif arg == "end":
                self.end = kwargs[arg]
        return self.save()

    def dataSerializer(self) -> json:
        result = {
            {"id": self.auctionId}: {
                "start": str(self.start),
                "end": str(self.end),
                "winner": {"name": self.winner.user.username},
                "initPrice": self.initPrice,
                "finalPrice": self.finalPrice,
                "item": self.item,
            }
        }

        return json.dumps(result)

    def truncatetx(self):
        if self.ethTx != "PENDING":
            return self.ethTx[:5] + " . . . " + self.ethTx[-5:]
        else:
            return self.ethTx

    def get_ending_time(self):
        if self.status == "o":
            time = timezone.localtime(self.start) + Timer_settings.time
            return time.strftime("%b. %d. %Y. %I:%M %p")
        else:
            return "Ended"

    def __str__(self) -> str:
        return str(self.auctionId)


def last_Prop(auctionId):
    lastProp = None
    try:
        lastProp = RedisServer.get_last_proposal(auctionId)["bid"]
    except:
        lastProp = Auction.objects.filter(pk=auctionId)[0].initPrice
    return lastProp


"""Signal configuration"""


@receiver(pre_delete, sender=Auction)
def model_deleter(sender, instance, using, **kwargs):
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.add_delete_from_watchList(auctionId=kwargs["origin"][0].pk, delete=True)
    return print(RedisServer.delete(key=kwargs["origin"][0].pk))


# Create your models here.
