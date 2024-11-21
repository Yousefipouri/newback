from django.db import models
from account.models import MyUser
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    isReligious = models.BooleanField(default=False)
    isNature = models.BooleanField(default=False)
    isHistorical = models.BooleanField(default=False)
    isIndoor= models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(MyUser, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(MyUser, related_name='disliked_posts', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for post: {self.post.title}"



class PostComment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()

    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(MyUser, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(MyUser, related_name='disliked_comments', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.body
