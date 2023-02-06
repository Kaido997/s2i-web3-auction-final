from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Auction, Profile, last_Prop
from django.contrib import messages
from .form import RegistrationForm, NewAuction
import json
from .tools import check_permission, RedisServer
from django.core.exceptions import BadRequest
from django.contrib.admin.views.decorators import staff_member_required
from .tasks import schedule_auction_end
from django.core.paginator import Paginator


def homepageView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            return redirect("homepage")
    else:
        allAuctions = Auction.objects.filter(status="o")

        return render(request, "auction/auction_view.html", {"auctions": allAuctions})


def registerView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.create(user)
            return redirect("homepage")
    else:
        form = RegistrationForm()
    return render(request, "auction/register_page.html", {"form": form})


@login_required(login_url="/")
def logoutView(request):
    logout(request)
    return redirect("homepage")


@login_required(login_url="/")
def auctionDetailView(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    currentProfile = Profile.objects.filter(user=request.user)[0]
    s = RedisServer()
    lastProp = last_Prop(auctionId=pk)
    if request.method == "POST":
        bid = int(request.POST["bid"])
        if bid >= lastProp + 1 and auction.status == "o":
            s.write(pk, request.user.username, bid)
            return redirect("details", pk=pk)
        else:
            if bid <= lastProp:
                messages.error(
                    request, message="The bid you entered is lower then last price"
                )
                return redirect("details", pk=pk)
            else:
                messages.error(request, message="Auction is closed")
                return redirect("details", pk=pk)

    return render(
        request,
        "auction/auction_detail.html",
        {"auction": auction, "lastProp": lastProp + 1},
    )


@login_required(login_url="/")
@check_permission
def profileView(request, username):
    currentProfile = Profile.objects.filter(user=request.user)[0]
    winnedauctions = Auction.objects.filter(winner=currentProfile)
    paginator = Paginator(winnedauctions, 5)
    pageNum = request.GET.get("page")
    pageObj = paginator.get_page(pageNum)
    winnedcounter = len(winnedauctions)
    return render(
        request,
        "auction/profile_page.html",
        {
            "winned": winnedauctions,
            "profile": request.user.username,
            "winnedcounter": winnedcounter,
            "page_obj": pageObj,
        },
    )


@login_required(login_url="/")
@check_permission
def watchlistView(request, username):
    currentProfile = Profile.objects.filter(user=request.user)[0]
    watchlist = [
        Auction.objects.get(pk=i) for i in json.loads(currentProfile.watchList)
    ]
    watchlistcounter = len(watchlist)
    return render(
        request,
        "auction/watchlist_page.html",
        {
            "watched": watchlist,
            "profile": request.user.username,
            "watchcounter": watchlistcounter,
        },
    )


@login_required(login_url="/")
def deleteFromWatchList(request, pk):
    currentProfile = Profile.objects.filter(user=request.user)[0]
    if not currentProfile.add_delete_from_watchList(auctionId=pk, delete=True):
        raise BadRequest
    return redirect("watchlist", username=request.user.username)


@login_required(login_url="/")
def addInWatchList(request, pk):
    currentProfile = Profile.objects.filter(user=request.user)[0]
    if Auction.objects.get(pk=pk).status == "o":
        if not currentProfile.add_delete_from_watchList(auctionId=pk):
            messages.error(request, "Item already in watchlist")
            return redirect("details", pk=pk)
        else:
            return redirect("watchlist", username=request.user.username)
    else:
        messages.error(request, "Auction closed")
        return redirect("details", pk=pk)


@login_required(login_url="/")
@staff_member_required(login_url="/")
def auctionNew(request):
    if request.method == "POST":
        form = NewAuction(request.POST)
        if form.is_valid():
            form.save()
            last_creation = Auction.objects.latest("pk")
            last_creation.auctionId = last_creation.pk
            last_creation.save()
            schedule_auction_end(last_creation)
            return redirect("homepage")
    else:
        form = NewAuction()
        return render(request, "auction/auctionNew.html", {"form": form})


# Create your views here.
