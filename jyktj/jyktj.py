import sys
import cx_Oracle as orcl

def jyktj(startdate='2017-04-01',enddate='2017-04-02',mzorzy='H',dept_name=''):
    hisdb = orcl.connect('hisuser/hisuser@192.168.0.10/orcl10')
    hiscursur = hisdb.cursor()
    if mzorzy == 'H':
        hissql = '''
        select * from
  (select b.dept_name as 科室名称,sum(a.amount) as 数量,a.item_name as 项目名称,'门诊' as 类别
 from inp_bill_detail a left join dept_dict b on a.PERFORMed_by=b.dept_code
 WHERE a.ITEM_CLASS='C'
 AND A.PERFORMed_BY='0726'
 and a.billing_date_time>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
 and a.billing_date_time<=to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')
 and b.dept_name like '%%%%%s%%%%'
 group by  b.dept_name,a.item_name
 union all
 select b.dept_name as 科室名称,sum(a.amount) as 数量,a.item_name as 项目名称,'住院' as 类别
 from outp_bill_items a left join dept_dict b on a.PERFORMed_by=b.dept_code
 WHERE a.ITEM_CLASS='C'
 AND A.PERFORMed_BY='0726'
 and a.visit_date>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
 and a.visit_date<=to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')
 and b.dept_name like '%%%%%s%%%%'
 group by  b.dept_name,a.item_name) A
 order by A.类别,A.数量 desc
''' % (startdate,enddate,dept_name,startdate,enddate,dept_name)
    elif mzorzy == 'Z':
        hissql = '''
 select b.dept_name as 科室名称,sum(a.amount) as 数量,a.item_name as 项目名称,'住院' as 类别
 from inp_bill_detail a left join dept_dict b on a.PERFORMed_by=b.dept_code
 WHERE a.ITEM_CLASS='C'
 AND A.PERFORMed_BY='0726'
 and a.billing_date_time>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
 and a.billing_date_time<=to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')
 and b.dept_name like '%%%%%s%%%%'
 group by  b.dept_name,a.item_name
 order by sum(a.amount) desc
 ''' % (startdate,enddate,dept_name)
    else:
        hissql = '''
 select b.dept_name as 科室名称,sum(a.amount) as 数量,a.item_name as 项目名称,'门诊' as 类别
 from outp_bill_items a left join dept_dict b on a.PERFORMed_by=b.dept_code
 WHERE a.ITEM_CLASS='C'
 AND A.PERFORMed_BY='0726'
 and a.visit_date>=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
 and a.visit_date<=to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss')
 and b.dept_name like '%%%%%s%%%%'
 group by  b.dept_name,a.item_name
 order by sum(a.amount) desc
 ''' % (startdate,enddate,dept_name)
    hiscursur.execute(hissql)
    jyktj = hiscursur.fetchall()
    return jyktj