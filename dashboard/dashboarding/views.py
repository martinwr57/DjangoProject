# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from dashboarding.models import Result, Device, ProductFilter, Dellinqdata
from django.http import HttpResponse
import django_filters

"""def index(request):
    latest_result_list = Result.objects.all().order_by('-timestamp')
    t = loader.get_template('dashboarding/index.html')
    c = Context({
        'latest_result_list':latest_result_list,
    })
    #output = ', '.join([p.question for p in latest_poll_list])
    #return HttpResponse(output)
    return HttpResponse(t.render(c))"""

def index(request):
    latest_result_list = Result.objects.all().order_by('serialnumber')[:5]
    latest_device_list = Device.objects.all().order_by('memorytype')

    return render_to_response('dashboarding/index.html', {'latest_result_list': latest_result_list, 'latest_device_list':latest_device_list})
    
    
def dellinqdata(request):
    f = ProductFilter(request.GET, queryset=Dellinqdata.objects.all())
    return render_to_response('dashboarding/dellinqdata_list.html', {'filter':f})
                                                             