from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import csv,codecs
from .lgszytj import lgszysf
from lgs.lgsmzzytj import lgsmzzytj

# Create your views here.
def index(request):
    return render(request,
     'zytj/index.html')

def zysfFreshtable(request):
    if request.is_ajax():
        startyear = int(request.GET.get('startyear'))
        startmonth = int(request.GET.get('startmonth'))
        startday = int(request.GET.get('startday'))
        endyear = int(request.GET.get('endyear'))
        endmonth = int(request.GET.get('endmonth'))
        endday = int(request.GET.get('endday'))
        dept = request.GET.get('dept')
        if dept == '老干所本所开单总院执行':
            islgs = False
        else:
            islgs = True
        zytj = lgsmzzytj('%s-%s-%s'%(startyear,startmonth,startday),'%s-%s-%s'%(endyear,endmonth,endday),isMZorZY=False,deptname='',isLGS=islgs)
        context = {'zytj':zytj,'startyear':startyear,'startmonth':startmonth,'startday':startday,'endyear':endyear,
                           'endmonth':endmonth,'endday':endday,'dept':dept}
        return render(request,
                              'zytj/zysfFreshtable.html',context)

def csvgen(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="老干所住院收费.csv'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    if request.is_ajax():
        startyear = int(request.GET.get('startyear'))
        startmonth = int(request.GET.get('startmonth'))
        startday = int(request.GET.get('startday'))
        endyear = int(request.GET.get('endyear'))
        endmonth = int(request.GET.get('endmonth'))
        endday = int(request.GET.get('endday'))
        dept = request.GET.get('dept')
        if dept == '老干所本所开单总院执行':
            islgs = False
        else:
            islgs = True
        zytj = lgsmzzytj('%s-%s-%s'%(startyear,startmonth,startday),'%s-%s-%s'%(endyear,endmonth,endday),isMZorZY=False,deptname='',isLGS=islgs)
        context = {'zytj':zytj,'startyear':startyear,'startmonth':startmonth,'startday':startday,'endyear':endyear,
                           'endmonth':endmonth,'endday':endday,'dept':dept}
    writer.writerow(['开单科室','执行科室','费用类别','收入'])
    for lgs in zytj:
        writer.writerow(list(lgs))
    return response