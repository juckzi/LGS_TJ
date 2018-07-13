import sys
import cx_Oracle as orcl

def lgsmzzytj(startdate='2017-04-01',enddate='2017-04-02',isMZorZY=True,deptname='',isLGS=True):
    hisdb = orcl.connect('hisuser/hisuser@192.168.0.10/orcl10')
    hiscursur = hisdb.cursor()
    if isMZorZY:
        hissql = '''
select a.performed_by, max(e.dept_name),a.class_on_reckoning,max(b.class_name) as FB,sum(a.costs) as costs
from outp_bill_items a left join RECK_ITEM_CLASS_DICT b on a.class_on_reckoning=b.class_code
left join outp_payments_money c on a.rcpt_no=c.rcpt_no
left join outp_rcpt_master d on a.rcpt_no=d.rcpt_no
left join dept_dict e on a.performed_by=e.dept_Code
left join v_acct_tally_master f on d.acct_no=f.acct_no
where
f.dept_code='0307'
and c.money_type='现金'
and f.bus_type='收费'
and f.acct_date>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
and f.acct_date<=to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')
and e.dept_name like '%%%%%s%%%%'
group by  a.class_on_reckoning,a.performed_by
order by  costs desc,a.performed_by
'''%(startdate,enddate,deptname)
        hiscursur.execute(hissql)
        mzsf = hiscursur.fetchall()
        return mzsf
    else:
        if isLGS: 
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