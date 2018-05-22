from django.shortcuts import render
from .models import VideoURL, VideoHistory
from .forms import DownloadVideoForm, LoginForm, RegisterForm
#from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import download_script as dc
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from .models import VideoHistory
from django.utils import timezone
from django.conf import settings
from os import sep as osSEP
# Create your views here.

def downloadform(request, videoPath):
    response = HttpResponse(content_type='video/ts')
    response['Content-Disposition'] = 'attachment; filename=%s' % videoPath
    return response

def index(request):
    #if request is GET
    videoHist = VideoHistory.objects.filter(video_owner = request.user.username)[:5]
    if request.method == 'POST':
        #list of downladed video files, last 5
        if 'download' in request.POST:
            if request.user.is_authenticated:
                form = DownloadVideoForm(request.POST)
                args = {}
                if form.is_valid():
                    #vchannel_name = TVChannel.objects.get(channel_short = request.POST.get('channel_name','')).channel_short
                    args['vchannel'] = request.POST.get('channel_name','')
                    args['vdate'] = str(datetime.strptime(request.POST.get('video_date',''), '%m/%d/%Y').strftime('%Y-%m-%d'))
                    args['vstart_time'] = str(request.POST.get('start_time','')) + ':01'
                    args['vend_time'] = str(request.POST.get('end_time','')) + ':01'
                    args['vfull_playlist'] = VideoURL.objects.get(url_code = 'playlist').video_url
                    args['vdownload_url'] = VideoURL.objects.get(url_code = 'dowloadList').video_url
                    args['username'] = request.user.username
                    fileName = dc.video_download(*args.values())
                    #return back empty form and new video list
                    context = {'form':DownloadVideoForm(), 'videoHist': videoHist}
                    #add new video to the videohistory table
                    videoPath = str(settings.MEDIA_URL) + args['username'] + osSEP + fileName
                    videoLog = VideoHistory(channel_short = args['vchannel'], video_datetime = timezone.now(),
                                            video_path = videoPath, video_owner = args['username'])
                    videoLog.save()
                    # return to the user "Save as..." dialog windows
                    downloadform(request, videoPath)
                    #after all process, return context with an initial form data
                    return render(request,'getvideo/index.html',context,)
                else:
                    context = {'form':form}
                    if form.has_error('channel_name', code = None):
                        context['channel_name_error'] = form.errors.get('channel_name')[0]

                    if form.has_error('video_date', code = None):
                        context['video_date_error'] = form.errors.get('video_date')[0]

                    if form.has_error('start_time', code = None):
                        context['start_time_error'] = form.errors.get('start_time')[0]

                    if form.has_error('end_time', code = None):
                        context['end_time_error'] = form.errors.get('end_time')[0]
                    context['videoHist'] = videoHist
                    return render(request,'getvideo/index.html',context,)
            else:
                url = '/accounts/login/'
                return HttpResponseRedirect(url)
        elif 'register' in request.POST:
            return HttpResponseRedirect('/')

    else:
        form = DownloadVideoForm()
        login_form = LoginForm()
        register_form = RegisterForm()
        context = {'form': form,'login_form': login_form,
                   'register_form': register_form}
        context['videoHist'] = videoHist
    return render(request,'getvideo/index.html',context,)
