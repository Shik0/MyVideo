from django.shortcuts import render
from .models import VideoURL
from .forms import DownloadVideoForm, LoginForm, RegisterForm
#from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import download_script as dc
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    if request.method == 'POST':
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
                    dc.video_download(*args.values())
                    context = {'ok':'Download Completed!'}
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

    return render(request,'getvideo/index.html',context,)

def downloadform(request):
    #form = DownloadVideoForm()
    #login_form = LoginForm()
    #register_form = RegisterForm()
    #context = {'form': form,'login_form': login_form, 'register_form': register_form}
    context = {'none':'none'}
    return render(request,'getvideo/index_cp.html',context,)
