from captcha.fields import CaptchaField
from django import forms

# 登录表单
from login.models import User, Profile


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    # captcha = CaptchaField(label='验证码')


# 注册表单
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


# 修改用户信息表单
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'cellphone', 'avatar', 'bio')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
