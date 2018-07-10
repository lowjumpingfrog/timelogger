import json
import requests
import urllib3
from django.conf import settings
import datetime as dt
from work_type.models import WorkCategory
from reasons.models import Reasons
from django.conf import settings
from django.db.models import Q

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_qgenda_shift(email,date):
	if not email or not date:
		return 'Invalid Lookup'

	shift = []
	login_error = ''
	get_error = ''
	credentials = {'email': settings.QGENDA_EMAIL, 'password': settings.QGENDA_PASSWORD}

	# try to login
	try:
	    login_request = requests.post(settings.QGENDA_LOGIN_ENDPOINT,data=credentials,verify=False,timeout=5)
	    login_request.raise_for_status()
	except requests.exceptions.HTTPError as errh:
	    login_error = "Http Error:"+ errh
	except requests.exceptions.ConnectionError as errc:
	    login_error = "Error Connecting:" + errc
	except requests.exceptions.Timeout:
	    login_error = "Timeout Error:" + errt
	except requests.exceptions.RequestException as err:
	    login_error = "OOps: Something Else" + err

	if login_error:
		#do some logging here
		return ''

	# deal with login response
	login_response = json.loads(login_request.text)
	access_token = login_response["access_token"]
	# form get request
	get_header = {'Authorization': 'bearer ' + access_token, 'Content-Type': 'application/json', 'Accept-Encoding': '*'}
	get_request = 'companyKey='+settings.QGENDA_COMPANY_KEY+'&startDate='+date+'&$select=Date,TaskAbbrev,StaffEmail&$filter=IsPublished&$filter=tolower(StaffEmail)eq\''+email+'\''

	#try the get request
	try:
	    get_response = requests.get(settings.QGENDA_GET_ENDPOINT,params=get_request,headers=get_header,timeout=5)
	    get_response.raise_for_status()
	except requests.exceptions.HTTPError as errh:
	    get_error = "Http Error:"+ errh
	except requests.exceptions.ConnectionError as errc:
	    get_error = "Error Connecting:" + errc
	except requests.exceptions.Timeout as errt:
	    get_error = "Timeout Error:" + errt
	except requests.exceptions.RequestException as err:
	    get_error = "OOps: Something Else" + err

	if get_error:
		# do some logging here
		return ''

	# deal with get response
	schedule_info = json.loads(get_response.text)

	if len(schedule_info) > 0 and 'TaskAbbrev' in schedule_info[0]:
		for row in schedule_info:
			shift.append(row["TaskAbbrev"])
		return ",".join(shift)
	else:
		#do some logging here
		return 'Nothing Found'

def get_pay_record(record):
	pay = 0
	memo = []
	day_filter = ''
	this_reason = list(Reasons.objects.filter(reason = record.reason).values('reason','billable','group_id'))[0]
	if this_reason['billable']:
		day_of_week = record.work_start_time.weekday()

		if record.work_start_time.date() in settings.SPS_HOLIDAYS:
			day_filter = 'hol'
		if day_of_week >= 0 and day_of_week < 5 and day_filter == '':
			day_filter = 'wkd'
		if day_of_week == 5 or day_of_week == 6 and day_filter == '':
			day_filter = 'wkend'

		work_cats = WorkCategory.objects.filter(group=this_reason['group_id']).filter(Q(day_flag = day_filter) | Q(day_flag = 'any')).values('work_category','start_time','stop_time','rate')


		for row in work_cats:
			pay_window = calculate_pay_window(row['start_time'],row['stop_time'],record.work_start_time.replace(second=0,microsecond=0),record.work_end_time.replace(second=0,microsecond=0))

			time = round(calculate_duration(pay_window[0],pay_window[1],record.work_start_time.replace(second=0,microsecond=0),record.work_end_time.replace(second=0,microsecond=0)),2)

			if time > 0:
				pay = pay + time*float(row['rate'])
				memo.append(str('{0:.2f}'.format(time)) + ' hrs @ $' + str(row['rate'])+'/hr')
		if len(memo) > 1:
			pay_memo = ', '.join(memo)
		else:
			if len(memo) == 1:
				pay_memo = str(memo[0])
			else:
				pay_memo = ''

		pay = '{0:.2f}'.format(pay)
	else:
		pay = 0
		pay_memo = ''
	return {'pay':pay,'pay_memo':pay_memo}


def calculate_duration(win_open,win_closed,work_start,work_end):
    duration = 0
    if work_start <= win_open:
        if  work_end <= win_closed:
            return (work_end - win_open)/ dt.timedelta(hours=1)
        if work_end >= win_closed:
            return (win_closed - win_open)/ dt.timedelta(hours=1)
    if work_start >= win_open:
        if  work_end <= win_closed:
            return (work_end - work_start)/ dt.timedelta(hours=1)
        if work_end >= win_closed:
            return (win_closed - work_start)/ dt.timedelta(hours=1)
    return duration

def calculate_pay_window(cat_start,cat_stop,work_start_datetime,work_end_datetime):

    work_start_date = work_start_datetime.date()
    work_start_time = work_start_datetime.time()
    work_end_date = work_start_datetime.date()

    if cat_start > cat_stop: # overnight
        if  work_start_date == work_end_date and dt.timedelta(hours = work_start_time.hour) > dt.timedelta(hours=12):
            win_open = dt.datetime.combine(work_start_date ,cat_start)
            win_closed = dt.datetime.combine((work_end_date + dt.timedelta(days=1)),cat_stop)
        else:
            win_open = dt.datetime.combine((work_start_date - dt.timedelta(days=1)),cat_start)
            win_closed = dt.datetime.combine(work_end_date,cat_stop)
    else:
        win_open = dt.datetime.combine(work_start_date,cat_start)
        win_closed = dt.datetime.combine(work_end_date,cat_stop)

    return([win_open,win_closed])
