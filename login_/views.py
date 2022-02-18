import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import hashlib

# Create your views here.
from login import models, forms
from login.forms import UserForm, EditUserForm, ProfileForm
from login.models import User, Profile


def check_login(fn):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_login', False):
            return fn(request, *args, **kwargs)
        else:
            # 获得用户当前访问的url，并传递给/user/login/
            next = request.get_full_path()
            red = HttpResponseRedirect('/login/login/?next=' + next)
            return red

    return wrapper


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("blog:index")
    if request.method == 'POST':
        message = "请检查填写的内容！"
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        userform = UserForm(data=request.POST)

        if userform.is_valid():
            try:
                username = userform.cleaned_data.get("username")
                password = userform.cleaned_data.get("password")
                user = User.objects.get(user_name=username)
            except:
                errormessage = "用户名不存在"
                context = {"errormessage": errormessage}
                return render(request, "login/login.html", context=context)

            if not user.email_confirmed:
                errormessage = '该用户还未经过邮件确认'
                context = {"errormessage": errormessage}
                return render(request, 'login/login.html', context=context)

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                request.session['name'] = user.name
                request.session['avatar_url'] = user.avatar.url
                return redirect('blog:index')
            else:
                errormessage = "密码不正确"
                context = {"errormessage": errormessage}
                return render(request, "login/login.html", context=context)
        else:
            errormessage = "登录验证失败"
            context = {"errormessage": errormessage}
            return render(request, "login/login.html", context=context)

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('login:index')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        errormessage = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                errormessage = '两次输入的密码不同'
                context = {"errormessage": errormessage}
                return render(request, 'login/register.html', context=context)
            else:
                same_name_user = models.User.objects.filter(user_name=username)
                if same_name_user:
                    errormessage = '用户名已经存在'
                    context = {"errormessage": errormessage}
                    return render(request, 'login/register.html', context=context)
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    errormessage = '该邮箱已经被注册了'
                    context = {"errormessage": errormessage}
                    return render(request, 'login/register.html', context=context)

                new_user = models.User()
                new_user.user_name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                errormessage = '请前往邮箱进行确认'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


@login_required(login_url='/login/login/')
def edit_user(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(id=id)

    if request.method == 'POST':
        if request.user != user:
            errormessage = "您没有权限修改次用户的信息"
            context = {"errormessage": errormessage}
            return render(request, "login/user_edit.html", context=context)
        # edit_user_form = EditUserForm(request.POST, request.FILES)

        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            profile.save()
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()

            request.session['name'] = user.name
            return redirect("blog:index")
        else:
            errormessage = "用户编辑表单输入有误。请重新输入"
            context = {"errormessage": errormessage}
            return render(request, "login/user_edit.html", context=context)
    elif request.method == 'GET':
        # edit_user_form = ProfileForm()
        # user.avatar.url = 'media/avatar/20220127/tom.jpg'
        profile_form = ProfileForm()
        context = {"profile_form": profile_form, 'profile': profile, "user": user}
        return render(request, "login/user_edit.html", context)
    else:
        errormessage = "您没有权限修改次用户的信息"
        context = {"errormessage": errormessage}
        return render(request, "login/user_edit.html", context=context)


@check_login
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/login')
    request.session.flush()
    # 或者使用如下方法
    # del request.session['is_login']
    return redirect('/login/index/')


# 密码加密
def hash_code(s, salt="login"):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


# 生成邮箱确认码
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.user_name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


# 发送确认码到邮箱
def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自<DATAEXPLORER>的注册确认邮件'

    text_content = '''感谢注册<DATAEXPLORER>，这里是YIXI的博客和教程站点，专注于Python技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/login/confirm/?code={}" target=blank>DATAEXPLORER</a>，\
                    这里是YIXI的博客站点，专注于Python技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 邮箱确认
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.create_time.replace(tzinfo=None)
    now = datetime.datetime.now().replace(tzinfo=None)
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.email_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
