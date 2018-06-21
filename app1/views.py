from django.shortcuts import render
from app1.models import Topic, Webpage, AccessRecord, User, UserProfileInfo
from app1.forms import NewUserForm, FormName, UserProfileInfoForm, UserForm

# Imports for login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout

# Create your views here.
def index(request):
  webpages_list = AccessRecord.objects.order_by('date')
  context_dict = {'text': 'hello world', 'number': 100}
  return render(request, 'app1/index.html', context=context_dict)

# Login Tutorial
@login_required
def special(request):
  return render(request, 'app1/special.html')

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))

def user_login(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user:
      if user.is_active:
        auth_login(request, user)
        return HttpResponseRedirect(reverse('index'))
      else:
        return HttpResponse("ACCOUNT DEACTIVATED")

    else:
      print("Someone tried to login and failed")
      print("Username: {} and password {}".format(username, password))
      return HttpResponse("Invalid login detailed supplied")

  else:
    return render(request, 'app1/login.html')


# Register Tutorial
def register(request):
  registered = False

  if request.method == "POST":
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      profile = profile_form.save(commit=False)
      profile.user = user # one to one rs

      if 'profile_pic' in request.FILES:
        profile.profile_pic = request.FILES['profile_pic']

      profile.save()
      registered = True

    else:
      print(user_form.errors, profile_form.errors)

  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()

  return render(request, 'app1/register.html',
    { 'user_form': user_form,
      'profile_form': profile_form,
      'registered': registered
    }
  )

# Templates tutorials
def other(request):
  my_dict = {'insert_me': "Hello I am from views.py for help"}
  return render(request, 'app1/other.html', context=my_dict)

def relative(request):
  return render(request, 'app1/relative_url_templates.html')

# Form/model tutorial
def user(request):
  form = NewUserForm()
  if request.method == "POST":
    form = NewUserForm(request.POST)
    if form.is_valid():
      form.save(commit=True)
      return index(request)
    else:
      print('ERROR FORM INVALID')

  #user_list = User.objects.order_by('first_name')
  #user_dict = {'user_records': user_list}

  return render(request, 'app1/user.html', {'form' : form})


def form_page(request):
  form = FormName()

  if request.method == 'POST':
    form = FormName(request.POST)
    if form.is_valid():
      # DO SOMETHING
      print("Validation Success!")
      print("NAME: "+form.cleaned_data['name'])
      print("EMAIL: "+form.cleaned_data['email'])
      print("TEXT: "+form.cleaned_data['text'])

  return render(request, 'app1/form_page.html', {'form': form})

