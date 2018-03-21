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
    latest_systems_list = Systems.objects.all().order_by('systemname')[:5]

    return render_to_response('dashboarding/systmes/index.html', {'latest_systems_list': latest_systems_list})
    
    
def detail(request, modelnumber_id):
    p = get_object_or_404(Result, pk=modelnumber_id)
    return render_to_response('dashboarding/detail.html', {'model': p})


def results(request, dashboard_id):
    return HttpResponse("You're looking at the results of poll %s." % dashboard_id)

def vote(request, dashboard_id):
    return HttpResponse("You're voting on poll %s." % dashboard_id)


def product_list(request):
    f = ProductFilter(request.GET, queryset=Device.objects.all())
    return render_to_response('dashboarding/template.html', {'filter':f})
                                                             


def dellinqdata(request):
    f = ProductFilter(request.GET, queryset=Dellinqdata.objects.all())
    return render_to_response('dashboarding/dellinqdata_list.html', {'filter':f})
                                                             