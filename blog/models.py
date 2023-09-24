from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='post_default.jpg', upload_to='post_pics')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)


    def __str__(self):
        return self.title


    def number_of_likes(self):
        return self.likes.count()

    
    def number_of_comments(self):
        return self.comments.count()

    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    posted_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"comment {self.id}"

    
    def get_absolute_url(self):
        return reverse('comments', kwargs={'pk': self.post.pk})


    def get_api_like_url(self):
        return reverse ('post_like_api', kwargs={'pk':self.post_like})


 

    




 

