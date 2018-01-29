import json
import requests
import urllib3
from django.conf import settings

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
	except requests.exceptions.Timeout:
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
	