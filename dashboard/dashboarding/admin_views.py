from dashboarding.models import Dellinqdata
from dashboarding.models import Systems
from dashboarding.models import Result
from dashboarding.models import Device
from dashboarding.models import Devicerev
from dashboarding.models import Codenames


from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404


def report(request):
    return render_to_response(
        "admin/dashboarding/dellinqdata/report.html",
        {'dellinqdata_list' : Dellinqdata.objects.all().order_by('headvendor')},
        RequestContext(request, {}),
    )
    
def sys_report(request):
    return render_to_response(
        "admin/dashboarding/systems/report.html",
        {'systems_list' : Systems.objects.all().order_by('modelname')},
        RequestContext(request, {}),
    )
    
def device_report(request, serialnumber, modelnumber):
    try:
        latest_result_list = Result.objects.filter(modelnumber=str(modelnumber))
    except Result.DoesNotExist:
        raise Http404
    try:
        dell_inquiry_page = Dellinqdata.objects.get(productserialnumber=str(serialnumber))
    except Dellinqdata.DoesNotExist:
        raise Http404
    try:
        device_info = Device.objects.get(serialnumber=str(serialnumber))
    except Device.DoesNotExist:
        raise Http404
    
    return render_to_response(
        'admin/dashboarding/device/report.html',
        {'device_info':device_info, 'dell_inquiry_page': dell_inquiry_page,
         'latest_result_list':latest_result_list})
    
 
    
report = staff_member_required(report)
