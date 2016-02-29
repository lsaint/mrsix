
import time, random, string, json
from hashlib import sha1
import requests

from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Experience, Share2
from .wechat_basic import WechatBasic

WB = WechatBasic(settings.WE_APPID, settings.WE_APPSECRET)


def index(request):
    return render(request, 'sixer/index.html')


@login_required(login_url=settings.LOGIN_URL2, redirect_field_name=None)
def index2(request):
    return render(request, 'sixer/index2.html')


@login_required(login_url=settings.LOGIN_URL2, redirect_field_name=None)
def products(request):
    ctx = {"login_url": settings.LOGIN_URL}
    return render(request, 'sixer/products.html', ctx)


@csrf_exempt
def share(request):
    if request.method == "POST":
        # 领取调过来的
        return render(request, 'sixer/share.html')
    return redirect(reverse('index'))


@login_required(login_url=settings.LOGIN_URL2, redirect_field_name=None)
def inspection(request):
    return render(request, 'sixer/inspection.html')


def share2(request, rid):
    r = get_object_or_404(Share2, rid=rid)
    ctx = {"name": r.user.last_name, "pic": r.user.email, "ret": r.result}
    return render(request, 'sixer/share2.html', ctx)


@login_required(login_url=settings.LOGIN_URL2, redirect_field_name=None)
@csrf_exempt
def result(request):
    if request.method == "POST":
        jn = json.loads(request.body.decode(encoding='UTF-8'))
        Share2.objects.create(user=request.user, rid=jn["rid"], result=jn["ret"])
        return HttpResponse("0")
    rid = ''.join(random.sample(string.ascii_letters, 16))
    return render(request, 'sixer/result.html', {"rid": rid})



def login_cb(request):
    userId = request.GET.get("userId")
    openId = request.GET.get("openId")
    headpic = request.GET.get("headpic")
    nickName = request.GET.get("nickName")
    user = authenticate(userId=userId, openId=openId, headpic=headpic, nickName=nickName)
    if user is None:
        return HttpResponse("login error")
    login(request, user)

    if Experience.objects.filter(userId=userId).exists():
        return redirect(reverse('index'))
    if save_ticket(request):
        Experience.objects.create(userId=userId)
        return render(request, 'sixer/share.html', {})
    return redirect(reverse('index'))


def wechat_cb(request):
    openId = request.GET.get("openId")
    headpic = request.GET.get("headpic")
    nickName = request.GET.get("nickName")
    user = authenticate(openId=openId, headpic=headpic, nickName=nickName)
    if user:
        login(request, user)
    return redirect(reverse('index2'))


#@login_required(redirect_field_name=None)
def get_discount(request):
    userId = request.user.username
    if Experience.objects.filter(userId=userId).exists():
        return HttpResponse("1")
    if save_ticket(request):
        Experience.objects.create(userId=userId)
        return HttpResponse("0")
    return HttpResponse("1")


def save_ticket(request):
    dt = {}
    t1 = int(time.time()*1000)
    dt["timestamp"] = str(t1)
    dt["failDate"] = str(t1 + 86400000) # 7days
    dt["nonce"] = ''.join(random.sample(string.ascii_letters, 16))
    dt["appId"] = "pazq1001"
    dt["activitId"] = "10011"
    dt["appSecret"] = "7879815081948772"
    dt["ticketOwner"] = request.user.username
    dt["ticketAmountArray"] = "5000"

    ss = "".join(sorted(dt.values()))
    dt["signature"] = sha1(ss.encode("utf-8")).hexdigest()
    dt.pop("appSecret")

    rep = requests.post(settings.TICKET_URL, data=dt)
    ret = rep.json()
    print("saveTicket: ", ret)

    return ret["responseCode"] == "0"


def wechat_ctx(request):
    context = {}
    context['timestamp'] = int(time.time())
    context['nonceStr'] = ''.join(random.sample(string.ascii_letters, 8))
    context['signature'] = WB.generate_jsapi_signature(
                        context['timestamp'],
                        context['nonceStr'],
                        request.build_absolute_uri())
    return context

