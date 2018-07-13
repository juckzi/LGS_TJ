import sys
import cx_Oracle as orcl

def lgszysf(startdate='2017-04-01',enddate='2017-04-02',deptname=''):
	hisdb = orcl.connect('hisuser/hisuser@192.168.0.10/orcl10')
	hiscursur = hisdb.cursor()
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