from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from studentskillsharing.models import Profile

# from .forms import SignUpForm


def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    auth_logout(request)
    return render(request, 'logout.html')


@login_required
def home(request):
    return render(request, 'registration/home.html')


@login_required
def search_nav(request):
    return render(request, 'registration/search_nav.html')


# @login_required
# def sign_up(request):
#
#     profile_instance = get_object_or_404(Profile, user=request.user)
#
#     if request.method == 'POST':
#         form = SignUpForm(data=request.POST, instance=profile_instance)
#         if form.is_valid():
#             profile_instance = form.save(commit=False)
#             profile_instance.user = request.user
#             profile_instance.save()
#
#         return redirect('/studentskillsharing/posts')
#     else:
#         form = SignUpForm(instance=profile_instance)
#         return render(request, 'registration/signup.html', {'form': form, "instance": profile_instance, })


# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
#         profs = Profile.objects.filter(first_name = query_string)
#         return render(request, 'search.html', { 'query_string': query_string, 'profiles': profs })
#     else:
#         return render(request, 'search.html', { 'query_string': 'Null', 'found_entries': 'Enter a search term' })
