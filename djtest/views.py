from django.contrib.auth import authenticate, login,logout
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import BaseUserCreationForm
from vote.models import Choice, Question,VoteRecord
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def loginapp(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 登录成功，进行重定向或其他操作
            return redirect("/vote/")  # 替换为你的成功页面URL
        else:
            # 无效登录，返回错误信息
            error_message = "Invalid username or password."
            return render(request, "loginapp.html", {"error_message": error_message})
    else:
        return render(request, "loginapp.html")

def registerapp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password1 == password2:
            # 检查数据库中是否存在相同的用户名
            if User.objects.filter(username=username).exists():
                error_message = "Username already exists."
                return render(request, "registerapp.html", {"error_message": error_message})
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                # 其他必要的操作，比如登录用户或重定向到其他页面
                return redirect('/login/')  # 注册成功后重定向到指定页面
        else:
            error_message = "Passwords do not match."
            return render(request, "registerapp.html", {"error_message": error_message})
    else:
        return render(request, 'registerapp.html')

def userinfo(request):
    user = request.user

    # 获取投票记录（这里假设有一个名为VoteRecord的模型）
    vote_records = VoteRecord.objects.filter(user=user)

    # 分页处理
    paginator = Paginator(vote_records, 10)  # 每页显示10条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    record = {
        'username': user.username,
        'vote_records': page_obj,
    }

    return render(request, 'userinfo.html', record)
def logoutapp(request):
    logout(request)
    return redirect('/login/')