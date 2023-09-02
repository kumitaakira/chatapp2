from django import forms
from django.contrib.auth.models import User
from .models import Account


# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

class AccountForm2(forms.ModelForm):
  
    
    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

class AddAccountForm(forms.ModelForm):
   
    
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('first_name','last_name','account_image')
        labels = {'last_name':"苗字",'first_name':"名前",'account_image':"写真アップロード",}




from.models import User,Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['to_user','content','sender']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-controlform-control-sm'}),
            
            'content':forms.Textarea(attrs={'class':'form-controlform-control-sm', 'rows':2}),
            'to_user': forms.HiddenInput(),  
            'sender': forms.HiddenInput(),   
              }
        labels = {
            'content':'メッセージ',
            
        }
        





