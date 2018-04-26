from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import TVChannel
#import datetime
from datetime import datetime, date, timedelta

class DownloadVideoForm(forms.Form):
    tv_list = [(chan.channel_short,chan.channel_long) for chan in TVChannel.objects.all()]
    tv_list.insert(0,(' ','Choose TV channel'))
    channel_name = forms.ChoiceField(choices = tv_list, required=True,
                 widget = forms.Select(attrs={'class':'custom-select text-muted','id':'chan','data-autoclose':'true'}))
    video_date = forms.DateField(input_formats=['%m/%d/%Y'], required = True,
                 widget = forms.TextInput(attrs={'class':'form-control text-muted', 'id':'datepicker','placeholder': 'MM/DD/YYYY',
                 'data-autoclose':'true'}))
    start_time = forms.TimeField(input_formats=['%H:%M'], required = True,
                 widget = forms.TextInput(attrs={'class':'form-control text-muted','placeholder': 'Start time'}))
    end_time = forms.TimeField(input_formats=['%H:%M'], required = True,
                 widget = forms.TextInput(attrs={'class':'form-control text-muted','placeholder': 'End time'}))
    
    
    def clean_channel_name(self):
        channel = self.cleaned_data['channel_name']
        tv_lst = [chan.channel_short for chan in TVChannel.objects.all()]
        
        if channel not in tv_lst:
            raise ValidationError(_('TV channel field is required.'))
            
        return channel  
    
    def clean_video_date(self):
        vdate = self.cleaned_data['video_date']
        
        if date.today() - timedelta(days = 7) > vdate:
            raise ValidationError(_('Video date should not be old more than 7 days'))
            
        return vdate   
    
    def clean_end_time(self):  
        end_t = self.cleaned_data['end_time']
        try:    
            #end_t = self.cleaned_data['end_time']
            start_t = self.cleaned_data['start_time']
        except:
            raise ValidationError(_(''))
            
        if end_t <= start_t:
            raise ValidationError(_('End time must be higher than start time'))
        
        minimum_video_duration  = timedelta(0,60) # one minute
        video_duration = datetime.combine(date.today(),end_t) - datetime.combine(date.today(),start_t) 
        
        if video_duration < minimum_video_duration:
            raise ValidationError(_('Minimum requires video duration is 1 minute.'))   
            
        return self.cleaned_data     
    
class LoginForm(forms.Form):
    user_name = forms.CharField(required=True,
                 widget = forms.TextInput(attrs={'class':'form-control text-muted','id':'id_username', 'placeholder': 'Username'}))
    user_password = forms.CharField(required = True,
                 widget = forms.PasswordInput(attrs={'class':'form-control text-muted', 'id':'id_password','placeholder': 'Password',}))
    
class RegisterForm(forms.Form):
    user_name = forms.CharField(required=True,
                 widget = forms.TextInput(attrs={'class':'form-control text-muted','id':'uname', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, min_length = 6, max_length = 40,
                 widget = forms.EmailInput(attrs={'class':'form-control text-muted','id':'email', 'placeholder': 'E-mail'}))    
    user_password = forms.CharField(required = True, min_length = 8,
                 widget = forms.PasswordInput(attrs={'class':'form-control text-muted', 'id':'upassword','placeholder': 'Password',}))