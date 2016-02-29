
from django.contrib.auth.models import User



class PingAnBackend(object):

    # username  <-> userId
    # password  <-> openId
    # email     <-> headpic
    # last_name <-> nickName

    def authenticate(self, userId="", openId="", headpic="", nickName=""):
        print("MrSixBackend authenticate", userId, openId, headpic, nickName)

        # 输入手机号回调, user可能已存在, 只是username(userId)为openId
        user = User.objects.filter(password=openId).first()
        if userId != "":
            if user:
                if user.username == openId:
                    user.username = userId
                    user.is_active = True
                    user.save()
            else:
                user = User(username = userId, password = (openId or "NULL"),
                                email = headpic, last_name = nickName)
                user.save()
        # 微信授权回调
        else:
            if not user:
                user = User(username = openId, password = openId,
                                email = headpic, last_name = nickName,
                                is_active = False)
                user.save()
        return user



    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            return None
