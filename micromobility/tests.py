from django.test import TestCase, Client
import json
from django.contrib.auth.models import User
from .models import Profile, Auction
from random import randint
import redis
import micromobility.views as view
from django.urls import reverse, resolve
vehicles = [
    "powered_standing_scooter",
    "powered_bicycle",
    "powered_seated_scooter",
    "powered_self-balacing_board",
    "powered_non-self-balancing_board",
    "powered_Skates",
]

def currentpk():
    try:
        latest = Auction.objects.latest('pk').pk
        return latest+1
    except:
        return 0


def start_redis_test_server():
        payload =  {
            'eta': 20, #seconds
            'initPrice': 400,
            'item': 'powered_bicycle',
            'itemId': randint(10000, 99999),
            'offersCounter': 0,
            'offerers': [],
            'status': 'open', 
        }

        testServer = redis.Redis(host='localhost', port=6380, db=0, charset="utf-8",decode_responses=True)
        testServer.delete('testAuctionId')
        testServer.set('testAuctionId', json.dumps(payload))
        return testServer

class Authtentication_TestCase(TestCase):

    def setUp(self) -> None:
        self.c: Client= Client()

    def test_user_can_register(self) -> None:
        response = self.c.post(
            '/register/', {'username': 'test', 'psw': 'testpsw'}, follow=True)
        self.assertEqual(response.status_code, 200, f"Status code is {response.status_code} should be 200")
    

    def test_user_can_login(self) -> None:
        User.objects.create_user(username="test", password="testpsw")
        response = self.c.post(
            '', {'username': 'test', 'psw': 'testpsw'}, follow=True)
        self.assertEqual(response.status_code, 200, f"Status code is {response.status_code} should be 200")

class User_ProfileTestCase(TestCase):

    def setUp(self) -> None:
        User.objects.create(username='test', password='testpassword')
        self.s = User.objects.all()
        Profile.create(user=self.s[0])
        self.c = Client()
        self.pk = currentpk()
        Auction.create(auctionId=self.pk, item="powered standing scooter", initPrice=500)
        
    def test_user_has_correct_profile(self) -> None:
        t = Profile.objects.filter(user=self.s[0])
        self.assertEqual(t[0].user, self.s[0])  


    def test_user_can_add_auction_to_watchlist(self) -> None:
        a = Auction.objects.latest('pk')
        p = Profile.objects.get(user=self.s[0])
        response = resolve("/register/")
        a.refresh_from_db()
        p.refresh_from_db()
        print(p.watchList)
        print(response)
        pass
    
    def test_user_can_delete_auctions_from_watchlist(self) -> None:
        pass
    
    def test_auction_should_delete_from_watchlist_on_complete(self) -> None:
        pass

    def test_auction_should_delete_from_watchlist_on_delete(self) -> None:
        pass    



# Create your tests here.
