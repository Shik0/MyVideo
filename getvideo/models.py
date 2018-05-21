from django.db import models
from django.conf import settings

# Create your models here.

class TVChannel(models.Model):
    """
    TV_channels = (
        ('aztv','Azərbaycan Televiziyası'),
        ('ictimai','İctimai Televiziyası'),
        ('atvaz','Azad Azərbaycan'),
        ('xazer','Xəzər TV'),
        ('idman','İdman Azərbaycan'),
    )
    """
    channel_long = models.CharField(max_length = 30, help_text = "TV channel long name")
    channel_short = models.CharField(max_length = 20, help_text = "TV channel short name")
    #channel = models.CharField(max_length = 30, help_text = "TV channel long name")

    def __str__(self):
        return self.channel_long

    class Meta:
        ordering = ['channel_long']

class VideoURL(models.Model):
    url_description = models.CharField(max_length = 255, help_text = "Description of the URL")
    video_url = models.CharField(max_length = 200, help_text = "Static URL's used to download video")
    url_code = models.CharField(max_length = 20, default = "", help_text = "URL identificator")

    def __str__(self):
        return "{0} {1}".format(self.video_url, self.url_description)

class VideoHistory(models.Model):
    channel_short = models.CharField(max_length = 20, help_text = "TV channel short name")
    video_datetime = models.DateTimeField(auto_now=True, help_text = "Download date and time")
    video_path = models.FilePathField(path = settings.MEDIA_ROOT, match="*.ts", allow_folders = True, recursive=True , help_text = "Video path")

    def __str__(self):
        return "{0} {1}".format(self.channel_short, self.video_datetime)
