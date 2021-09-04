from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """Temat poznawany przez użytkownika."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    header_image = models.ImageField(blank=True, null=True, upload_to="images/")

    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego."""
        return self.text

    def delete(self):
        """ Usuwa zdjęcie tematu."""
        self.header_image.delete()
        super().delete()


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, blank=True, null=True)
    facebook_url = models.CharField(max_length=255, blank=True, null=True)
    twitter_url = models.CharField(max_length=255, blank=True, null=True)
    insta_url = models.CharField(max_length=255, blank=True, null=True)
    pinterest_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def delete(self):
        """ Usuwa zdjęcie uzytkownika."""
        self.profile_pic.delete()
        super().delete()


class Entry(models.Model):
    """Konkretne informacje o postepie w nauce. """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    data_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Zwraca reprezentacje modelu w postaci ciągu tekstowego"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"
