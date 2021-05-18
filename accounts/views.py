from django.http.request import HttpRequest
from django.http.response import HttpResponse
from accounts.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from .forms import RegistrationForm, CookForm, UserForm
from .models import UserProfile
from category.models import Category
from cookbook.filters import RecipeFilter



def registerPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']

            UserProfile.objects.create(
            	user=user,
            )

            current_site = get_current_site(request)
            subject = 'SoYummy! Veryfication link'
            message = render_to_string('accounts/verification_email.html',  {
                'user': user,
                'current_site': current_site, 
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            receiver = email
            mail = EmailMessage(subject, message, to=[receiver])
            mail.send()
            return redirect('/?command=verification')
    else:
        form = RegistrationForm()
    context ={
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'The activation was successful! Now you can start using my app!')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Link is invalid! Sorry ...')
        return redirect('accounts:register')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('cookbook:recipes')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


@login_required
def logoutPage(request):
	logout(request)
	return redirect('home')


@login_required
def userProfilePage(request):
  cook = request.user.userprofile
  recipes = cook.creator.all()

  # if request.action == 'DELETE':

  context = {
    'cook': cook,
    'recipes': recipes,
  }
  return render(request, 'accounts/user_profile.html', context)


@login_required
def editUserPage(request):
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


# def userPage(request, user_slug=None, category_slug=None):
  # cook = UserProfile.objects.get(id=idU)
  # recipes = None
  # if category_slug:
  #   category = get_object_or_404(Category, slug=category_slug)
  #   recipes = cook.creator.filter(category=category)
  # else:
  #   recipes = cook.creator.order_by('-data_created')
  # context = {
  #   'cook': cook,
  #   'recipes': recipes,
  # }
  # return render(request, 'accounts/user.html', context)


@login_required
def userPage(request, user_slug=None, category_slug=None):
  recipes = None
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



def send_email(request, email, user, html, subject):
  current_site = get_current_site(request)
  message = render_to_string(f'accounts/{html}.html',  {
      'user': user,
      'current_site': current_site, 
      'uid': urlsafe_base64_encode(force_bytes(user.pk)),
      'token': default_token_generator.make_token(user),
  })
  receiver = email
  mail = EmailMessage(subject, message, to=[receiver])
  mail.send()

  
def forgertPassword(request):
  if request.method == 'POST':
    email = request.POST['emial']
    if User.objects.filter(email=email):
      user = User.objects.get(email__exact=email)
      send_email(request, email, user, 'password_email','New password')
      return redirect('/?command=reset_password')
    else:
      messages.error(request, 'Account does not exist!')
      return redirect('accounts:forget_password')

  context = {
  }
  return render(request, 'accounts/forget_password.html', context)

def resetPassword(request, uid64, token):
  try: 
    uid = urlsafe_base64_decode(uid64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    return redirect('accounts:new_password')
  else:
    messages.error(request, 'This link has been expired!')
    return redirect('accounts:login')


def newPassword(request):
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
            return redirect('accounts:newPassword')
    else:
        return render(request, 'accounts/reset_password.html')
