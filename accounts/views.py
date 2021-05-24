from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .forms import RegistrationForm, CookForm, UserForm
from .models import UserProfile
from category.models import Category
from cookbook.filters import RecipeFilter


def send_email(request, email, user, html, subject):
    current_site = get_current_site(request)
    message = render_to_string(f'accounts/{html}.html', {
        'current_site': current_site,
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    receiver = email
    mail = EmailMessage(subject, message, to=[receiver])
    mail.send()


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']

            UserProfile.objects.create(
                user=user,
            )
            send_email(request, email, user, 'verification_email', 'SoYummy! Verification link')
            return redirect('/?command=verification')
        # else handled in html
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Activation was successful! Now you can start using my application!')
        return redirect('accounts:login')
    else:
        messages.error(request, 'The link is invalid! Sorry ...')
        return redirect('accounts:register')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('cookbook:recipes')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'accounts/login.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('home')


@login_required
def user_profile_page(request):
    cook = request.user.userprofile
    recipes = cook.creator.all()

    context = {
        'cook': cook,
        'recipes': recipes,
    }

    return render(request, 'accounts/user_profile.html', context)


@login_required
def edit_user_page(request):
    cook = request.user.userprofile
    user = request.user
    cook_form = CookForm(instance=cook)
    user_form = UserForm(instance=user)

    if request.method == 'POST':
        cook_form = CookForm(request.POST, request.FILES, instance=cook)
        user_form = UserForm(request.POST, instance=user)
        if cook_form.is_valid() and user_form.is_valid():
            cook_form.save()
            user_form.save()
            return redirect('accounts:user_profile')

    context = {
        'cook': cook,
        'cook_form': cook_form,
        'user_form': user_form
    }

    return render(request, 'accounts/edit_user.html', context)


@login_required
def user_page(request, user_slug=None, category_slug=None):
    if user_slug:
        cook = get_object_or_404(UserProfile, slug=user_slug)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            recipes = cook.creator.filter(category=category).order_by('-creation_date')
        else:
            recipes = cook.creator.order_by('-creation_date')
        myFilter = RecipeFilter(request.GET, queryset=recipes)
        recipes = myFilter.qs
    else:
        return redirect('cookbook:recipes')

    context = {
        'cook': cook,
        'recipes': recipes,
        'myFilter': myFilter,
    }

    return render(request, 'accounts/user.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email):
            user = User.objects.get(email__exact=email)  # Important to get User instance, not QuerySet instance
            send_email(request, email, user, 'password_email', 'New password')
            return redirect('/?command=reset_password')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('accounts:forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uidb = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uidb)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = uidb
        return redirect('accounts:new_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('accounts:login')


def new_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('accounts:new_password')
    else:
        return render(request, 'accounts/reset_password.html')
