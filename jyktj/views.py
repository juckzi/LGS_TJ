from django.shortcuts import render
from django.http import HttpResponse
from .jyktj import jyktj
from datetime import datetime
import csv,codecs
# Create your views here.
def index(request):
    month = datetime.today().month
    year = datetime.today().year
    jyktj = ''
    context = {'year':year,'month':month,'tjgz':tjgz}
    return render(request,
        'jyktj/tjgz.html',context)

def csvgen(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="老干所检验科统计收费.csv'
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
        checked = request.GET.get('checked')
        if dept == '全所科室':
            dept = ''
        tjgz = jyktj('%s-%s-%s'%(startyear,startmonth,startday),'%s-%s-%s'%(endyear,endmonth,endday),mzorzy=checked,dept_name=dept)
        context = {'tjgz':tjgz,'startyear':startyear,'startmonth':startmonth,'startday':startday,'endyear':endyear,
                       'endmonth':endmonth,'endday':endday,'dept':dept}

        writer.writerow(['科室名称','数量','项目名称','类别'])
        for lgs in tjgz:
             writer.writerow(list(lgs))
        return response

def tjgzfreshtable(request):
    if request.is_ajax():
        startyear = int(request.GET.get('startyear'))
        startmonth = int(request.GET.get('startmonth'))
        startday = int(request.GET.get('startday'))
        endyear = int(request.GET.get('endyear'))
        endmonth = int(request.GET.get('endmonth'))
        endday = int(request.GET.get('endday'))
        dept = request.GET.get('dept')
        checked = request.GET.get('checked')
        if dept == '全所科室':
            dept = ''
        tjgz = jyktj('%s-%s-%s'%(startyear,startmonth,startday),'%s-%s-%s'%(endyear,endmonth,endday),mzorzy=checked,dept_name=dept)
        context = {'tjgz':tjgz,'startyear':startyear,'startmonth':startmonth,'startday':startday,'endyear':endyear,
                       'endmonth':endmonth,'endday':endday,'dept':dept}
     
        return render(request,
                          'jyktj/tjgzFreshtable.html',context)





