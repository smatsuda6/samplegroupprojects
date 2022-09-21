from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class Skill(models.Model):
    skill_title = models.CharField(max_length=100)
    skill_school = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.skill_title


class Profile(AbstractUser):
    skills = models.ManyToManyField(Skill)
    profile_image = models.ImageField(blank=True,
                                      null=True,
                                      default="generic_profile_image.png")

    follower_count = models.PositiveIntegerField(default=0)

    profile_showall = models.BooleanField(blank=True, null=True, default=True)
    profile_showmost = models.BooleanField(blank=True, null=True)
    profile_shownone = models.BooleanField(blank=True, null=True)

    posts_searchall = models.BooleanField(blank=True, null=True, default=True)
    posts_searchmost = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        kwargs = {
            'username': self.username
        }
        return reverse('profile', kwargs=kwargs)

    def get_skill_list(self):
        skills_qs = self.skills.all().values()
        if skills_qs.count() == 0:
            return "SKILLS: None specified yet."
        skill_list = "SKILLS: "
        for i, skill in enumerate(skills_qs):
            if i:
                skill_list += "; "
            skill_list += skill['skill_title']
        return skill_list

    def photo_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return '/media/generic_profile_image.png'


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200, verbose_name=_("title"))
    post_text = models.TextField(max_length=2500, verbose_name=_(""))

    date_created = models.DateTimeField(default=timezone.now, verbose_name=_("date created"))
    date_published = models.DateTimeField(blank=True, null=True, verbose_name=_("date published"))
    is_published = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    date_last_modified = models.DateTimeField(blank=True, null=True, verbose_name=_("date last modified"))


    # num_likes is updated with a reciever every time a post is saved. 
    likes = models.ManyToManyField(Profile, related_name="likes")
    num_likes = models.PositiveIntegerField(default=0) 


    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ['-date_published', '-num_likes']

    def get_num_likes(self):
        return self.likes.count()

    def publish(self):
            if len(self.post_text) == 0 or len(self.post_title) == 0:
                    raise ValueError('ERROR: Post must have a title and text in order to publish.')
            elif self.author is None:
                    raise ObjectDoesNotExist("Error: user not logged in or user does not exist. " +
                                             "Cannot publish post without an author.")
            if not self.is_published:
                self.date_published = timezone.now()
                self.date_last_modified = timezone.now()
                self.is_published = True
            else:
                self.date_last_modified = timezone.now()
                self.is_edited = True
            self.save()

    def get_absolute_url(self):
        kwargs = {
            'author': self.author.username,
            'id': self._get_pk_val(),
        }

        return reverse('post_detail', kwargs=kwargs)

    def get_post_likes(self):
        return Like.objects.filter(post=self).count()

    def __str__(self):
        return self.post_title


class ModelManager(models.Manager):
    def all(self):
        qs = Comment.objects.filter(parent=None)
        return qs


class Comment(models.Model):
    author = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=225, verbose_name=_(""))
    date_published = models.DateTimeField(blank=True, null=True, verbose_name=_("date published"))
    objects = ModelManager()

    class Meta:
        ordering = ['-date_published']

    def publish(self):
        if len(self.comment_text) == 0:
            raise ValueError('ERROR: Post must have a title and text in order to publish.')
        elif self.author is None:
            raise ObjectDoesNotExist("Error: user not logged in or user does not exist. " +
                                     "Cannot publish comment without an author.")
        self.date_published = timezone.now()
        self.save()

    # get replies to comment
    def children(self):
        return Comment.objects.filter(parent=self)

    def is_parent(self):
        if self.parent is not None:
            return False
        return True	

    #def __str__(self):
        #return str(self.comment_text)


@receiver(pre_save, sender=Post)
def default_subject(sender, instance, **kwargs):
    if instance.pk is not None: 
        instance.num_likes = instance.get_num_likes()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=timezone.now())


class Rating(models.Model):
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="rating_rater")
    ratee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rating_ratee")
    aggregate_rating = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=timezone.now())


class Connection(models.Model):
    connector = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name="connection_connector")
    connectee = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name="connection_connectee")
    timestamp = models.DateTimeField(auto_now_add=timezone.now())


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, 
                                 on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="receiver")
    message_text = models.TextField(max_length=2000, verbose_name=_(""))
    message_sent_date = models.DateTimeField(blank=True, null=True, verbose_name=_("date sent"))

    class Meta:
        ordering = ['-message_sent_date']

    def send(self):
        if len(self.message_text) == 0:
            raise ValueError('ERROR: Message must content in order to send')
        elif (self.sender is None) | (self.reciever is None):
            raise ObjectDoesNotExist("Error: user not logged in or user does not exist. " +
                                     "Cannot send message without a sender or receiver.")
        self.message_sent_date = timezone.now()
        self.save()
