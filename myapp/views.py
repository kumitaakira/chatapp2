from django.shortcuts import render
from django.views.generic import TemplateView # テンプレートタグ
from .forms import AccountForm,AccountForm2, AddAccountForm# ユーザーアカウントフォーム

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from .models import Account,User
from django.db.models import Q

def index(request):
    return render(request, "myapp/index.html")


def setting(request):
    params={
        'title':'設定',
    }
    return render(request, "myapp/setting.html",params)

def password(request):
    return render(request,'myapp/password.html',{'title':'password'})


    #ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                params = {
                          'UserID' : request.user,
                          'data': Account.objects.exclude(user=request.user),
                          
                }

    # データをテンプレートに渡す
                return render(request, 'myapp/friends.html', params)
                
                
                
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'myapp/login.html')


#ログアウト
@login_required 
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect('Logout')
   
#ホーム
@login_required
def home(request):
    params = {"UserID":request.user,}
    return render(request, "myapp/friends.html",context=params)


#新規登録
class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    #Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"myapp/signup.html",context=self.params)

    #Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        #フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"myapp/signup.html",context=self.params)
    


@login_required
def talk_room_back(request):
    params = {
        'data': Account.objects.exclude(user=request.user),
        'UserID':request.user,
        }

    # データをテンプレートに渡す
    return render(request, 'myapp/friends.html', params)
                
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .forms import MessageForm
from .models import Message


from django.shortcuts import render
from .models import Message
from django.db.models import QuerySet






def talk_room(request):
     # 適切なトークルームIDを設定してください
    
    messages = Message.objects.filter(to_user=request.user).order_by('pub_date').reverse()

    params = {
        'messages': messages,
        
    }
    

    return render(request, 'myapp/talk_room.html', params)



##実験的に作ってみた　トークルーム試作版＃＃
from .models import Account, Message
from .forms import AccountForm , MessageForm
from django.core.paginator import Paginator

def message(request,sender):
    if (request.method == 'POST'):
        obj = Message()
        content=request.POST.copy()
        content['sender']=request.user
        three=User.objects.filter(username=sender).values('id')[:1]
        content['to_user']=three
        form = MessageForm(content, instance=obj)
        form.save()
        
        return redirect('message',sender=sender)
    one=request.user
    two=User.objects.filter(username=sender).values('id')[:1]
    data = Message.objects.filter(to_user=request.user,sender=two).order_by('pub_date').reverse()
    data2 = Message.objects.filter(Q(to_user=request.user) & Q(sender=two) | Q(to_user=two) & Q(sender=request.user)).order_by('pub_date').reverse()

   
    params = {
        'title':'Message',
        'form':MessageForm(),
        'data':data2,
        'sender':sender,
        
    }

    return render (request,'myapp/message.html',params)

def change(request):
    obj=Account.objects.get(user=request.user)
    obj2=User.objects.get(username=request.user)
    if(request.method =='POST'):
        account=AccountForm2(request.POST,instance=obj2)
        addacount=AddAccountForm(request.POST,instance=obj)
        account.save()
        addacount.save()
        return redirect('complete')
    params={
        'title':'その他の変更',
        'form':AccountForm2(instance=obj2),
        'form2':AddAccountForm(instance=obj),
    }
    return render(request,'myapp/change.html',params)

def complete(request):
    return render(request,'myapp/complete.html')



