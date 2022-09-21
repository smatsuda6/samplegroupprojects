import datetime
import re

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.views import generic
from notifications.signals import notify
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .forms import CommentForm, EditPostForm, PostForm, UploadProfilePictureForm
from django.contrib.auth import get_user_model, logout as auth_logout
from .forms import CommentForm, PostForm, ReplyCommentForm
from .models import Comment, Post, Profile, Like, Connection
from .forms import CommentForm, PostForm, ProfilePrivacyForm
from .models import Comment, Post, Profile, Like, Connection, Skill


# Imports For Search
from django.db.models import Q
from functools import reduce
import operator

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat
import boto3


def redirect_new_users(request):
    if request.user.last_login - request.user.date_joined <= datetime.timedelta(seconds=1):
        return redirect('new_user_settings')
    return redirect('posts')


def new_user_settings(request):
    profile = get_object_or_404(Profile, username=request.user.username)
    if request.method == 'POST':
        privacy = request.POST.get('showmyid')
        if privacy == 'all':
            profile.profile_showall = True
            profile.profile_showmost = None
            profile.profile_shownone = None
        elif privacy == 'most':
            profile.profile_showall = None
            profile.profile_showmost = True
            profile.profile_shownone = None
        else:
            profile.profile_showall = None
            profile.profile_showmost = None
            profile.profile_shownone = True
        privacy = request.POST.get('searchmyposts')
        if privacy == 'all':
            profile.posts_searchall = True
            profile.posts_searchmost = None
        elif privacy == 'most':
            profile.posts_searchall = None
            profile.posts_searchmost = True
        profile.save()
        return redirect('/studentskillsharing/new_user_skills/')

    return render(request, 'studentskillsharing/new_user_settings.html')


def new_user_skills(request):
    schools = Skill.objects.values_list('skill_school', flat=True).distinct().order_by('skill_school')
    skills = Skill.objects.all().order_by('skill_title')

    if request.method == "POST":
        if 'skills-add' in request.POST:
            added_skills = request.POST.getlist('skillchoice')
            prof = get_object_or_404(Profile, username=request.user.username)
            for skill in added_skills:
                prof.skills.add(get_object_or_404(Skill, skill_title=skill))
            prof.save()
            return redirect('/studentskillsharing/recommendations/')

    return render(request, 'studentskillsharing/new_student_skills.html', {'schools': schools, 'skills': skills})


def recommendations(request):
    prof = get_object_or_404(Profile, username=request.user.username)
    skill_qs = prof.skills.all()
    matching_profs = Profile.objects.filter(skills__in=skill_qs).exclude(username=request.user.username).order_by('-follower_count').distinct()[:10]
    backup_profs = Profile.objects.all().exclude(username=request.user.username).order_by('-follower_count').distinct()[:10]

    connected_list = Connection.objects.filter(connectee__in=matching_profs, connector=request.user).values()
    id_list = []
    for found_profile in connected_list:
        id_list.append(found_profile['connectee_id'])
    already_connected_match = Profile.objects.filter(pk__in=id_list)

    connected_list = Connection.objects.filter(connectee__in=backup_profs, connector=request.user).values()
    id_list = []
    for found_profile in connected_list:
        id_list.append(found_profile['connectee_id'])
    already_connected_backup = Profile.objects.filter(pk__in=id_list)


    context = {

        'matching_profs': matching_profs,
        'backup_profs': backup_profs,
        'already_connected_match': already_connected_match,
        'already_connected_backup': already_connected_backup,

    }

    return render(request, 'studentskillsharing/recommendations.html', context)



def user_settings(request):
    profile = get_object_or_404(Profile, username=request.user.username)
    settings_applied = False

    if request.method == 'POST':
        if request.POST.get('showmyid'):
            privacy = request.POST.get('showmyid')
            if privacy == 'all':
                profile.profile_showall = True
                profile.profile_showmost = None
                profile.profile_shownone = None
            elif privacy == 'most':
                profile.profile_showall = None
                profile.profile_showmost = True
                profile.profile_shownone = None
            else:
                profile.profile_showall = None
                profile.profile_showmost = None
                profile.profile_shownone = True
            profile.save()

            show_all_boolean = profile.profile_showall
            show_most_boolean = profile.profile_showmost
            show_none_boolean = profile.profile_shownone
            search_all_boolean = profile.posts_searchall
            search_most_boolean = profile.posts_searchmost
            settings_applied = True

            context = {

                'profile': profile,
                'show_all_boolean': show_all_boolean,
                'show_most_boolean': show_most_boolean,
                'show_none_boolean': show_none_boolean,
                'search_all_boolean': search_all_boolean,
                'search_most_boolean': search_most_boolean,
                'settings_applied': settings_applied,

            }

            return render(request, 'studentskillsharing/user_settings.html', context)
        if request.POST.get('searchmyposts'):
            privacy = request.POST.get('searchmyposts')
            if privacy == 'all':
                profile.posts_searchall = True
                profile.posts_searchmost = None
            elif privacy == 'most':
                profile.posts_searchall = None
                profile.posts_searchmost = True
            profile.save()

            show_all_boolean = profile.profile_showall
            show_most_boolean = profile.profile_showmost
            show_none_boolean = profile.profile_shownone
            search_all_boolean = profile.posts_searchall
            search_most_boolean = profile.posts_searchmost
            settings_applied = True

            context = {

                'profile': profile,
                'show_all_boolean': show_all_boolean,
                'show_most_boolean': show_most_boolean,
                'show_none_boolean': show_none_boolean,
                'search_all_boolean': search_all_boolean,
                'search_most_boolean': search_most_boolean,
                'settings_applied': settings_applied,

            }

            return render(request, 'studentskillsharing/user_settings.html', context)
    else:
        show_all_boolean = profile.profile_showall
        show_most_boolean = profile.profile_showmost
        show_none_boolean = profile.profile_shownone
        search_all_boolean = profile.posts_searchall
        search_most_boolean = profile.posts_searchmost

        context = {

            'profile': profile,
            'show_all_boolean': show_all_boolean,
            'show_most_boolean': show_most_boolean,
            'show_none_boolean': show_none_boolean,
            'search_all_boolean': search_all_boolean,
            'search_most_boolean': search_most_boolean,

        }
        return render(request, 'studentskillsharing/user_settings.html', context)


def edit_skills(request):
    schools = Skill.objects.values_list('skill_school', flat=True).distinct().order_by('skill_school')
    skills = Skill.objects.all().order_by('skill_title')

    if request.method == "POST":
        if 'skills-add' in request.POST:
            added_skills = request.POST.getlist('skillchoice')
            prof = get_object_or_404(Profile, username=request.user.username)
            for skill in added_skills:
                prof.skills.add(get_object_or_404(Skill, skill_title=skill))
            prof.save()
            return redirect(request.user.get_absolute_url())
        else:
            added_skills = request.POST.getlist('skillchoice')
            prof = get_object_or_404(Profile, username=request.user.username)
            print(added_skills)
            for skill in added_skills:
                prof.skills.remove(get_object_or_404(Skill, skill_title=skill))
            prof.save()
            return redirect(request.user.get_absolute_url())

    return render(request, 'studentskillsharing/edit_skills.html', {'schools': schools, 'skills': skills})


@login_required
def profile(request, username):


    requested_profile = get_object_or_404(Profile, username=username)
    skill_qs = requested_profile.skills.all()
    user_posts = Post.objects.filter(author=requested_profile).order_by('-date_published')
    followers = Connection.objects.filter(connectee=requested_profile).count()
    following = Connection.objects.filter(connector=requested_profile).count()
    user_follow_status = Connection.objects.filter(connector=request.user, connectee=requested_profile).exists()

    client = boto3.client(
        's3',
        aws_access_key_id='AKIAIIQH747JZ5ZFDPIA',
        aws_secret_access_key='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',
    )
    try:
        client.get_object(Bucket='3240-Profile-Pictures'.lower(), Key=username + '.jpg')
        profile_picture_url = 'https://s3.amazonaws.com/3240-profile-pictures/' + username + '.jpg'
    except Exception as ex:
        profile_picture_url = None

    is_users_profile = requested_profile.get_username() == request.user.get_username()

    context = {
        'requested_profile': requested_profile,
        'skill_qs': skill_qs,
        'user_posts': user_posts,
        'user_follow_status': user_follow_status,
        'is_users_profile': is_users_profile,
        'followers': followers,
        'following': following,
        'profile_picture_url': profile_picture_url,
    }

    return render(request, 'studentskillsharing/profile.html', context)


def upload_profile_picture(request, username):
    if request.user.username != username:
        return HttpResponse("You can not upload a profile picture you do not own")

    if request.method == 'POST':
        form = UploadProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_picture = request.FILES['profile_picture']
            conn = S3Connection('AKIAIIQH747JZ5ZFDPIA', 'spbKHrm8U2TV22pCuPEqKaByXlRQ63oMxz/dQTkE')
            bucket = conn.get_bucket('3240-Profile-Pictures'.lower())
            k = Key(bucket)
            k.key = username + '.jpg'
            k.set_contents_from_file(profile_picture)
            return redirect(request.user.get_absolute_url())
    else:
        form = UploadProfilePictureForm()
    return render(request, 'studentskillsharing/upload_profile_picture.html', {'form': form, 'user': request.user})


class PostListView(generic.ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        following = []
        if not self.request.user.is_authenticated:
            return context

        for connection in Connection.objects.filter(connector=self.request.user):
            following.append(connection.connectee.username)

        following.append(self.request.user.username)

        context['post_list'] = Post.objects.filter(author__username__in=following).order_by('-date_published')
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-date_published')
        return ordering


def sort_by_newest(request):
    following = []
    if not request.user.is_authenticated:
        context = {'post_list': None}
        return render(request, 'studentskillsharing/post_list.html', context)
    for connection in Connection.objects.filter(connector=request.user):
        following.append(connection.connectee.username)

    following.append(request.user.username)

    post_list = Post.objects.filter(author__username__in=following).order_by('-date_published')
    context = {'post_list': post_list}
    return render(request, 'studentskillsharing/post_list.html', context)


def sort_by_oldest(request):
    following = []
    if not request.user.is_authenticated:
        context = {'post_list': None}
        return render(request, 'studentskillsharing/post_list.html', context)
    for connection in Connection.objects.filter(connector=request.user):
        following.append(connection.connectee.username)

    following.append(request.user.username)

    post_list = Post.objects.filter(author__username__in=following).order_by('date_published')
    context = {'post_list': post_list}
    return render(request, 'studentskillsharing/post_list.html', context)


def sort_by_top(request):
    following = []
    if not request.user.is_authenticated:
        context = {'post_list': None}
        return render(request, 'studentskillsharing/post_list.html', context)
    for connection in Connection.objects.filter(connector=request.user):
        following.append(connection.connectee.username)

    following.append(request.user.username)

    post_list = Post.objects.filter(author__username__in=following).order_by('-num_likes')
    context = {'post_list': post_list}
    return render(request, 'studentskillsharing/post_list.html', context)


def sort_by_bottom(request):
    following = []
    if not request.user.is_authenticated:
        context = {'post_list': None}
        return render(request, 'studentskillsharing/post_list.html', context)
    for connection in Connection.objects.filter(connector=request.user):
        following.append(connection.connectee.username)

    following.append(request.user.username)

    post_list = Post.objects.filter(author__username__in=following).order_by('num_likes')
    context = {'post_list': post_list}
    return render(request, 'studentskillsharing/post_list.html', context)


def post_detail_view(request, author, id):
    profile = get_object_or_404(Profile, username=request.user.username)
    post = get_object_or_404(Post, pk=id)
    like_status = ''
    if post.likes.filter(username=profile.username).exists():
        like_status = ' liked'
    if request.method == 'POST':

        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = profile
            comment.post = post
            comment.parent = None
            try: # Check if comment has a parent
                parent_id = request.POST.get('parent_id')
                comment.parent = Comment.objects.filter(pk=parent_id).first()
            except:
                comment.parent = None
            notify.send(sender=comment.author,
                        recipient=post.author,
                        verb=request.user.first_name + ' ' + request.user.last_name + ' commented on your post: "' + comment.comment_text + '"',
                        timestamp=timezone.now(),
                        action_object=post)
            comment.publish()
            return redirect(post.get_absolute_url())

    comment_form = CommentForm()
    reply_comment_form = ReplyCommentForm()
    comments = Comment.objects.filter(post=post).filter(parent=None)
    context = {
        'post': post,
        'comment_form': comment_form,
        'reply_comment_form': reply_comment_form,
        'comments': comments,
        'like_status': like_status,
    }
    return render(request, 'studentskillsharing/post_detail.html', context)


def like_post(request):
    context = RequestContext(request)
    post_id = None
    if request.method == 'GET':
        post_id = request.GET.get('post_id')

    likes = 0
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        user_like_status = Like.objects.filter(post=post, user=request.user).exists()
        if not user_like_status:
            new_like = Like.objects.create(user=request.user, post=post, timestamp=timezone.now())
            new_like.save()
            notify.send(sender=request.user,
                        recipient=post.author,
                        verb=request.user.first_name + ' ' + request.user.last_name + " liked your post.",
                        timestamp=new_like.timestamp,
                        action_object=post)
        else:
            Like.objects.filter(user=request.user, post=post).delete()
        likes = "Liked by: " + str(Like.objects.filter(post=post).count()) + " users"
        user_like_status = not user_like_status
        new_data = {"likes": likes, "user_like_status": user_like_status}

    return JsonResponse(new_data)


def connect_with_profile(request):
    context = RequestContext(request)
    profile_id = None
    if request.method == 'GET':
        profile_id = request.GET.get('profile_id')

    if profile_id:
        profile = get_object_or_404(get_user_model(), username=profile_id)
        user_follow_status = Connection.objects.filter(connector=request.user, connectee=profile).exists()
        if not user_follow_status:
            new_connection = Connection.objects.create(connector=request.user,
                                                       connectee=profile,
                                                       timestamp=timezone.now())
            new_connection.save()
            notify.send(sender=request.user,
                        recipient=profile,
                        verb=request.user.first_name + ' ' + request.user.last_name +" followed your profile.",
                        timestamp=new_connection.timestamp,
                        action_object=profile)
        else:
            Connection.objects.filter(connector=request.user, connectee=profile).delete()
        profile.follower_count = Connection.objects.filter(connectee=profile).count()
        profile.save()
        user_follow_status = not user_follow_status

    followers = str(Connection.objects.filter(connectee=profile).count()) + " Followers"
    new_data = {"user_follow_status": user_follow_status, 'followers': followers}

    return JsonResponse(new_data)


def notifications(request):
    profile = get_user_model().objects.get(username=request.user.username)
    unread_notifications_list = profile.notifications.unread()
    read_notifications_list = profile.notifications.read()
    return render(request, 'studentskillsharing/notifications.html', {'read_notifications_list': read_notifications_list, 'unread_notifications_list': unread_notifications_list})

@login_required
def post_new(request):
    profile = get_object_or_404(Profile, username=request.user.username)

    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = profile
            post.publish()

            return redirect(post.get_absolute_url())
    else:
        # loads the form
        form = PostForm()
        return render(request, 'studentskillsharing/create_post.html', {'form': form})


# allows you to edit posts that aren't your own
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponse("You can not edit a post you do not own")

    if request.method == 'POST':
        form = EditPostForm(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
        return redirect(post.get_absolute_url())
    else:
        # loads the form
        form = EditPostForm(instance=post)
        return render(request, 'studentskillsharing/edit_post.html', {'form': form, 'post': post, })


@login_required
def like_post(request, pk):
    profile = get_object_or_404(Profile, username=request.user.username)
    post = get_object_or_404(Post, pk=pk)

    if post.likes.filter(username=profile.username).exists():
        post.likes.remove(profile)
    else:
        post.likes.add(profile)
        if request.user != post.author:
            notify.send(sender=request.user,
                        recipient=post.author,
                        verb=request.user.first_name + " " + request.user.last_name + " liked your post.",
                        timestamp=timezone.now(),
                        action_object=post)
    post.save()
    return redirect(post.get_absolute_url())


@login_required
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if comment.author != request.user:
        return HttpResponse("You can not delete a comment you do not own")
    elif request.method == 'POST':
        comment.comment_text = "COMMENT DELETED"
        comment.publish()
        return redirect(post.get_absolute_url())
    return render(request, 'studentskillsharing/comment_delete.html', {'post': post, 'comment': comment, })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponse("You can not delete a post you do not own")
    elif request.method == 'POST':
        post.delete()
        return redirect('posts')
    return render(request, 'studentskillsharing/post_delete.html', {'post': post, })

'''
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        profs = Profile.objects.filter(first_name = query_string)
        return render(request, 'search.html', { 'query_string': query_string, 'profiles': profs })
    else:
        return render(request, 'search.html', { 'query_string': 'Null', 'found_entries': 'Enter a search term' })
'''

def logout(request):
    auth_logout(request)
    return render(request, 'studentskillsharing/logout.html')


#----------------------------------------#
#          SEARCH FUNCTIONALITY          #
#----------------------------------------#
# https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
# https://www.webforefront.com/django/modelqueriesbysql.html
# https://wellfire.co/learn/simple-search-manager-methods/ - NOT USED
# https://stackoverflow.com/questions/35126136/filter-multiple-keywords
def search(request):
    keywords = request.GET['q'].split()

    connected_list = Connection.objects.filter(connectee=request.user).values()
    id_list = []
    for found_profile in connected_list:
        id_list.append(found_profile['connector_id'])
    followed_by = Profile.objects.filter(pk__in=id_list)

    qs = Q()
    qs2 = Q()
    qs3 = Q()
    if keywords:
        qs &= reduce(lambda x, y: x | y, [Q(first_name__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(last_name__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(username__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(email__icontains=word) for word in keywords])
        qs2 &= reduce(lambda x, y: x | y, [Q(post_title__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(post_text__icontains=word) for word in keywords]) | reduce(operator.and_, [Q(author__username__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(author__first_name__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(author__last_name__icontains=word) for word in keywords])
        qs3 &= reduce(lambda x, y: x | y, [Q(skill_title__icontains=word) for word in keywords]) | reduce(lambda x, y: x | y, [Q(skill_school__icontains=word) for word in keywords])

    if not re.search('\d+', request.GET['q']):
        user_filter = Profile.objects.filter(qs)
    else:
        user_filter = Profile.objects.filter(qs).filter(profile_shownone=None)

    initial_skill_filter = Skill.objects.filter(qs3)
    user_skill_filter = Profile.objects.filter(skills__in=initial_skill_filter).exclude(username=request.user.username).distinct()

    return render(request, 'studentskillsharing/search_user_list.html', {'user_filter': user_filter, 'post_filter': Post.objects.filter(qs2), 'user_skill_filter': user_skill_filter, 'followed_by': followed_by})
