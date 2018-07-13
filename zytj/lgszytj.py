import sys
import cx_Oracle as orcl

def lgszysf(startdate='2017-04-01',enddate='2017-04-02',islgs=True):
    hisdb = orcl.connect('hisuser/hisuser@192.168.0.10/orcl10')
    hiscursur = hisdb.cursor()
    if islgs: 
        	hissql = '''
select b.dept_name 开单科室,d.dept_name 执行科室,c.subj_name 费用类别 ,sum(costs) 收入
from Inp_Bill_Detail a left join dept_dict b on a.ordered_by=b.dept_code
left join tally_subject_dict c on a.subj_code=c.subj_code
left join dept_dict d on a.performed_by=d.dept_code
where b.branch_code='02'
and d.branch_code='02'
and a.billing_date_time>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
and a.billing_date_time<=to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')
group by c.subj_name ,b.dept_name,d.dept_name
order by 收入 desc
'''%(startdate,enddate)
    else:
        hissql = '''
select b.dept_name 开单科室,d.dept_name 执行科室,c.subj_name 费用类别 ,sum(costs) 收入
from Inp_Bill_Detail a left join dept_dict b on a.ordered_by=b.dept_code
left join tally_subject_dict c on a.subj_code=c.subj_code
left join dept_dict d on a.performed_by=d.dept_code
where b.branch_code='02'
and d.branch_code<>'02'
and a.billing_date_time>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
and a.billing_date_time<=to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')
group by c.subj_name ,b.dept_name,d.dept_name
order by 收入 desc
'''%(startdate,enddate)
    hiscursur.execute(hissql)
    zytj = hiscursur.fetchall()
    return zytj