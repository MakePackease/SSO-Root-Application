from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

from django.views.generic.base import TemplateView
from .forms import UserRegisterForm,UserUpdateForm
#from articles.models import Article
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import JsonResponse
from jwt import ExpiredSignatureError, InvalidTokenError, decode  # Import from jwt library directly

def get_active_user_count():
    active_users = User.objects.filter(is_active=True)
    usernames = [user.username if user.is_authenticated else 'Anonymous' for user in active_users]
    return usernames

def index(request):
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    if request.user.is_authenticated:
        request.session['username'] = request.user.username
    else:
        request.session['username'] = 'Anonymous'

    count = request.session.get('visit_count', 0)
    request.session['visit_count'] = count + 1

    context = {'username': request.session['username'], 'visit_count': count}
    return render(request, 'home.html', context)


@csrf_exempt
def login_(request):
    return render(request, 'base.html' )
    if request.method == 'GET':
        try:
            # data = json.loads(request.body)
            # username = data.get('username')
            # password = data.get('password')
            # Handle authentication and login logic here
            user = authenticate(request, username='sahil_amin', password='sahil@123')
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                # return redirect('http://127.0.0.1:8000/parent/')
                return redirect(f'http://127.0.0.1:5000/')
            else:
                return HttpResponse("Invalid credentials", status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



class HomePageView(TemplateView):
    template_name = "home.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["latest_articles"] = Article.objects.all()[:5]
    #     return context

from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
def get_logged_in_users(request):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_ids.append(user_id)
    users = User.objects.filter(id__in=user_ids)
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    print(users_list)
    # return JsonResponse(users_list, safe=False)
    active_users = User.objects.filter(is_active=True)
    usernames = []
    for user in active_users:
        if user.is_authenticated :
            usernames.append(user.username)
    return JsonResponse(usernames, safe=False)  
   
from django.contrib import messages
def register(request):
	# now we have to creae a form which will pass to views
	if request.method == 'POST':
		# form = UserCreationForm(request.POST)
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			# form.save(force_insert=False)
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your Accounted Has been Created! You are able to login now :)')
			# messages.success(request, f'Accounted Created for {username} !')#we have got our flashed message here
			# now we have to redirect our user to another page as his account is created
			# return redirect('blog-home')
			return redirect('http://127.0.0.1:8000/parent/')
		else:
			print("Please Enter Correct Credentials")
	else:
		# form = UserCreationForm()
		form = UserRegisterForm()
	# print("sahil",form)    
	return render(request, 'register.html', {'form': form})


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

from .token import CustomAccessToken  # Import the custom token class
def login_as_user(request, username):
    print('view arrive from login')
    try:
        user = User.objects.get(username=username)
        request.session["username"] = username
        login(request, user)
        # request.session["member_id"] = user
        # refresh = RefreshToken.for_user(user)
        # token = refresh.access_token
        # token['sub'] = user.username  # Add the 'sub' claim
        # token['user_id'] = user.id 
        # token = str(token)
        token = CustomAccessToken.for_user(user)
        token['sub'] = user.username  # Add the 'sub' claim
        token_str = str(token)
        context = {
            'flask_app_url' : f'http://127.0.0.1:5000/protected',
            'token': token,
        }
        flask_app_url = f'http://127.0.0.1:5000/protected?token={token_str}'
        # return redirect(flask_app_url)
        # print(token)
        # from django.http import HttpResponse
        # response = HttpResponse("Cookie set successfully!")
        # response.set_cookie('sso-sessionid', 'abc123', max_age=3600)
        request.session['token'] = 'abc123'
        # Optionally set expiry for the session data
        request.session.set_expiry(1209600)  # 1209600 seconds = 14 days
        return render(request, 'redirect_with_token.html', context)
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=404)