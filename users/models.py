from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", 
         related_name = 'followed_by',
         symmetrical = False,
         blank = True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField()


    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})


    def number_of_follows(self):
        return self.follows.count()


    
    def number_of_followers(self):
        return self.followed_by.count()
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)