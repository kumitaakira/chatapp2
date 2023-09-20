
from django.db import models
# ユーザー認証
from django.contrib.auth.models import User

# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス(1vs1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    mail_address = models.EmailField(max_length=200,default='example@example.com')
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    account_image = models.ImageField(upload_to="profile_pics",blank=True)

    def __str__(self):
        return self.user.username  
    

from django.db import models
from django.contrib.auth.models import User



class TalkRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Message(models.Model):
     to_user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
     title = models.CharField(max_length=100,null=True,blank=True)
     content = models.CharField(max_length=300)
     pub_date = models.DateTimeField(auto_now_add=True)
     sender=models.ForeignKey(User,on_delete=models.CASCADE, related_name='message_sender')
     
     def __str__(self):
         return '<Message:id=' + str(id) +','+str(self.sender)+'to'+str(self.to_user) + '(' + str(self.pub_date) + ')>'
     
     