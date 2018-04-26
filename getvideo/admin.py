from django.contrib import admin
from .models import TVChannel, VideoURL

# Register your models here.
@admin.register(TVChannel)
class TVChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_short', 'channel_long')
    fields = ['channel_short', 'channel_long']

@admin.register(VideoURL)
class VideoURLAdmin(admin.ModelAdmin):
    list_display = ('url_description', 'video_url', 'url_code')
    fields = ['url_description', 'video_url', 'url_code']
