from django.shortcuts import render
from django.http import HttpResponse
#from .lgsmzsf import lgsmzsf
from lgs.lgsmzzytj import lgsmzzytj
from datetime import datetime
import csv,codecs
# Create your views here.
def index(request):
	month = datetime.today().month
	year = datetime.today().year
	#mztj = lgsmzzytj('%s-%s-01'%(year,month),'%s-%s-31'%(year,month),'老干所放射科')
	mztj = ''
	context = {'year':year,'month':month,'mztj':mztj}
	return render(request,
	'mztj/lgsmzsf.html',context)
	
def MZTJfreshtable(request):
	if request.is_ajax():
		startyear = int(request.GET.get('startyear'))
		startmonth = int(request.GET.get('startmonth'))
		startday = int(request.GET.get('startday'))
		endyear = int(request.GET.get('endyear'))
		endmonth = int(request.GET.get('endmonth'))
		endday = int(request.GET.get('endday'))
		dept = request.GET.get('dept')
		if dept == '全所科室':
			dept = ''
		mztj = lgsmzzytj('%s-%s-%s'%(startyear,startmonth,startday),'%s-%s-%s'%(endyear,endmonth,endday),isMZorZY=True,deptname=dept,isLGS=False)
		context = {'mztj':mztj,'startyear':startyear,'startmonth':startmonth,'startday':startday,'endyear':endyear,
		'endmonth':endmonth,'endday':endday,'dept':dept}
		return render(request,
		'mztj/mzsfFreshtable.html',context)

def csvgen(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="老干所门诊收费.csv'
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
        if dept == '全所科室':
            dept = ''
        mztj = lgsmzzytj('%s-%s-%s'%(startyear,startmonth,startday),'%s-%s-%s'%(endyear,endmonth,endday),isMZorZY=True,deptname=dept,isLGS=False)
        rouname = ['科室名称','费用类别','收入']
        writer.writerow(rouname)
        for lgs in mztj:
            writer.writerow([lgs[1],lgs[3],lgs[4]])
    return response
    