from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Profile, Post, Message, Like
from .views import CommentForm, PostForm, like_post



class ProfileModelTest(TestCase):
    def test_profile_to_string(self):
        user = Profile(username="xyz")
        self.assertEqual("xyz", user.__str__())


class PostModelTest(TestCase):
    def setUp(self):
        profile = Profile(username='xyz')
        profile.save()

    def test_publish_without_message_body(self):
        try:
            profile = Profile.objects.get(username='xyz')
            post = Post(post_title="New post")
            post.publish()
            self.fail("test fail: len exception was not caught.")
        except ValueError:
            pass

    def test_publish_with_message_body(self):
        try:
            profile = Profile.objects.get(username='xyz')
            post = Post(post_title="New post", post_text="Hi! this is a new post", author=profile,)
            post.publish()
            pass
        except Exception:
            self.fail("test fail: publish() created an unexpected exception.")

    def test_publish_without_author(self):
        try:
            post = Post(post_title="New post", post_text="Hi! this is a new post",)
            post.publish()
            self.fail("test fail: publish() did not catch the NoAuthorException.")
        except ObjectDoesNotExist:
            pass


class CommentModelTest(TestCase):
    def setUp(self):
        profile = Profile(username='xyz')
        profile.save()
        post = Post(post_title="New_post", post_text="Hi! this is a new post", author=profile,)
        post.publish()

    def test_publish_valid_comment(self):
        try:
            profile = Profile.objects.get(username='xyz')
            post = Post.objects.get(post_title="New_post")
            comment = Comment(author=profile, comment_text='hello', post=post)
            comment.publish()
            pass
        except Exception:
            self.fail("test fail: comment.publish() caused an unexpected exception.")

    def test_publish_without_author(self):
        try:
            post = Post.objects.get(post_title="New_post")
            comment = Comment(comment_text='hello', post=post)
            comment.publish()
            self.fail("test fail: publish did not catch the NoAuthorException.")
        except Exception:
            pass
    
    def test_publish_without_text(self):
        form = CommentForm(data={'comment_text': "this is a comment", 'author': None})
        try:
            profile = Profile.objects.get(username='xyz')
            post = Post.objects.get(post_title="New_post")
            comment = Comment(author=profile, comment_text='', post=post)
            comment.publish()
            self.fail("test fail: did not catch ValueError for null comment")
        except Exception:
            pass

class LikeTest(TestCase):
    def test_LikePost(self):
        profile = Profile(username='xyz')
        profile.save()
        post = Post(post_title="New_post", post_text="Hi! this is a new post", author=profile,)
        post.publish()

        profile2 = Profile(username='abc')
        profile2.save()
        post.likes.add(profile2)
        post.save()
        self.assertTrue(post.num_likes == 1)

    def test_LikePostMultiple(self):
        profile = Profile(username='xyz')
        profile.save()
        post = Post(post_title="New_post", post_text="Hi! this is a new post", author=profile,)
        post.publish()

        n = 100
        for i in range(n):
            p = Profile(username='iter'+str(i))
            p.save()
            if i % 2 == 0:
                post.likes.add(p)
                post.save()
        self.assertTrue(post.num_likes == n/2)
            
    def test_LikePost_not_valid(self):
        profile = Profile(username='xyz')
        profile.save()
        post = Post(post_title="New_post", post_text="This post has no likes!", author=profile)
        post.publish()
        self.assertFalse(post.num_likes == 1)


class PostFormTest(TestCase):
    def test_PostForm_Valid(self):
        form = PostForm(data={'post_title': 'Example title', 'post_text': 'example text'})
        self.assertTrue(form.is_valid())

    def test_PostForm_NotValid(self):
        form = PostForm(data={'post_text': 'example text'})
        self.assertFalse(form.is_valid())
        # all fields, virginia.edu address should be valid


class CommentFormTest(TestCase):
    def test_CommentForm_valid(self):
        form = CommentForm(data={'comment_text': "this is a comment"})
        self.assertTrue(form.is_valid())

    def test_CommentForm_not_valid(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())


class ReplyCommentFormTest(TestCase):
    def test_ReplyCommentForm_valid(self):
        form = CommentForm(data={'comment_text': "this is a comment"})
        self.assertTrue(form.is_valid())

    def test_ReplyCommentForm_not_valid(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())


class PostViewTest(TestCase):
    def setUp(self):
        profile = Profile.objects.create_user('xyz', 'temp@virginia.edu', 'temp_password')
        profile.save()

	# Should redirect unathenticated users
    def test_post_url_not_authenticated(self):
        response = self.client.get(reverse('post_new'))
        self.assertEquals(response.status_code, 302)

class MessageModelTest(TestCase):
    def setUp(self):
        profile1 = Profile(username='xyz')
        profile1.save()
        profile2 = Profile(username='qwerty')
        profile2.save()
        message = Message(sender=profile1, reciever=profile2, message_text="This is a message",)
        message.send()

    def test_publish_valid_message(self):
        try:
            profile1 = Profile.objects.get(username='xyz')
            profile2 = Profile.objects.get(username='qwerty')
            message = Message(sender=profile1, reciever=profile2, message_text="This is a message", )
            message.send()
            pass
        except Exception:
            self.fail("test fail: message.send() caused an unexpected exception.")
    
    def test_invalid_sender(self):
        try:
            profile2 = Profile.objects.get(username='qwerty')
            bad_message = Message(sender=None, reciever=profile2, message_text="Failure")
            bad_message.send()
            self.fail("test fail: did not catch invalid sender")
        except Exception:
            pass
    
    def test_invalid_receiver(self):
        try:
            profile1 = Profile.objects.get(username='xyz')
            bad_message = Message(sender=profile1, reciever=None, message_text="Failure")
            bad_message.send()
            self.fail("test fail: did not catch invalid receiver")
        except Exception:
            pass
    
    def test_invalid_message(self):
        try:
            profile1 = Profile.objects.get(username='xyz')
            profile2 = Profile.objects.get(username='qwerty')
            message = Message(sender=profile1, reciever=profile2, message_text="", )
            message.send()
            self.fail("test fail: did not catch invalid message")
        except Exception:
            pass
 


