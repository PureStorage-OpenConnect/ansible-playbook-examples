import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from base64 import b64encode
import os
import sys
import json
import getpass
from optparse import OptionParser
from datetime import datetime, timedelta
import time
from time import gmtime, strftime, strptime
from operator import itemgetter, attrgetter

# Global Variables
VERSION = '1.0.0'
HEADER = 'Pure Storage List Protection Group Snapshot Replication (' + VERSION + ')'
BANNER = ('=' * 132)
DEBUG_LEVEL = 0
VERBOSE_FLAG = False
QUITE_FLAG = False 

COOKIE = ''

def create_session(flashArray, user, password, api_token):
    global COOKIE

    # Set-up HTTP header
    userAgent = 'Jakarta Commons-HttpClient/3.1'
    hdrs= {'Content-Type' : 'application/json', 'User-agent' : userAgent, 'Cookie' : COOKIE}
  
    #Establish Session, if no token provide need to create an API token first
    
    if user:
        data = {
               'password': user,
               'username': password
               }
        params = json.dumps(data)
        path = '/api/1.12/auth/apitoken'
        url = 'https://%s%s'%(flashArray,path)
    
        # Perform action
        response = requests.post(url, params, headers=hdrs, verify=False)

        COOKIE = response.cookies
    
        if DEBUG_LEVEL == 2:
            print('Status', response.status_code)
            print('Reason', response.reason)
            print('Text', response.text)
            print('Data', response.json)
            print('HTTP Header:', response.headers)
            print('Cookie', COOKIE)
            print('')
    
        if (response.reason) != 'OK':
            print(BANNER)
            sys.exit('Exiting: invalid username / password combination')
                
        jsonString = response.text
        jsonData = json.loads(jsonString)
    
        api_token = (jsonData['api_token'])

    data =  {
            'api_token': api_token
            }
    
    params = json.dumps(data)
    path = '/api/1.12/auth/session'
    url = 'https://%s%s'%(flashArray,path)

    # Perform action
    if not QUITE_FLAG:
        print('Attempting to create session')

    response = requests.post(url, params, headers=hdrs, verify=False)

    COOKIE = response.cookies

    if DEBUG_LEVEL == 2:
        print('Status', response.status_code)
        print('Reason', response.reason)
        print('Text', response.text)
        print('Data', response.json)
        print('HTTP Header:', response.headers)
        print('Cookie', COOKIE)
        print('')

    if (response.reason) != 'OK':
        print(BANNER)
        sys.exit('Exiting: Unable to establish session')

    jsonString = response.text
    jsonData = json.loads(jsonString)

    if not QUITE_FLAG and VERBOSE_FLAG:
        print(json.dumps(jsonData, sort_keys=False, indent=4))

    name = (jsonData['username'])
    welcome = 'Welcome ' + name

    if not QUITE_FLAG:
        print(welcome)


def post_url(flashArray,path,params):
    # Set-up HTTP header
    userAgent = 'Jakarta Commons-HttpClient/3.1'
    hdrs= {'Content-Type' : 'application/json', 'User-agent' : userAgent}
    url = 'https://%s%s'%(flashArray,path)
    
    # Perform action
    response = requests.post(url, params, headers=hdrs, cookie=COOKIE, verify=False)
    
    if DEBUG_LEVEL != 0:
        print('Response Status:', response.status_code)
        print('Reason:', response.reason)
        print('Text', response.text)
        print('Data', response.json)
        print('HTTP Header:', response.headers)
        print('Cookie', COOKIE)
        print('')
   
    jsonString = response.text
    jsonData = json.loads(jsonString)
    return(jsonData)


def get_url(flashArray,path,params):
    # Set-up HTTP header
    userAgent = 'Jakarta Commons-HttpClient/3.1'
    hdrs= {'Content-Type' : 'application/json', 'User-agent' : userAgent}
    url = 'https://%s%s'%(flashArray,path)
    payload = params

    # Perform action
    response = requests.get(url, headers=hdrs, cookies=COOKIE, verify=False)
    
    if DEBUG_LEVEL != 0:
        print('Response Status:', response.status_code)
        print('Reason:', response.reason)
        print('Text', response.text)
        print('Data', response.json)
        print('HTTP Header:', response.headers)
        print('Cookie:', COOKIE)
    
    jsonString = response.text
    jsonData = json.loads(jsonString)
    return(jsonData)


def list_pgsnaps(flashArray,pgroup,limit):
    data = ''
    params = json.dumps(data)
    
    if pgroup != '':
        path = '/api/1.12/pgroup?names=%s&snap=true&transfer=true&sort=created-&limit=%s'%(pgroup,limit)
    else:
        path = '/api/1.12/pgroup?snap=true&transfer=true&sort=created-&limit=%s'%(limit)

    # Perform action
    jsonData = get_url(flashArray,path,params)

    r =  str(jsonData)

    if (r[3:15]) == 'pure_err_key':
        pure_err_code = jsonData[0]['pure_err_code']
        msg = 'Exiting: ' + pgroup + ' ' + jsonData[0]['msg']
        print(BANNER)

        sys.exit(msg)

    if VERBOSE_FLAG:
        print(json.dumps(jsonData, sort_keys=False, indent=4))

    # Count of returned rows
    res = len(jsonData)

    if res == 0:
        print('No Snaps found')
    else:
        x = 0
        
        if not QUITE_FLAG:
            print(BANNER)
            print('{0:40} {1:60} {2:20} {3:10}'.format('Source', 'Snap Name', 'Created', 'Progress'))
            print(BANNER)

        while (x<res):
            #
            source = (jsonData[x]['source'])
            name = (jsonData[x]['name'])
            progress = (jsonData[x]['progress'])
            physical = (jsonData[x]['physical_bytes_written'])
            cdate = (jsonData[x]['created'])
            c1 = cdate[0:10]
            c2 = cdate[11:19]
            c3 = c1 + ' ' + c2

            c4 = strptime(c3,'%Y-%m-%d %H:%M:%S')
            created = strftime('%d/%m/%Y %H:%M:%S', c4)
            
            if not QUITE_FLAG:
                print('{0:40} {1:60} {2:20} {3:10}'.format(source, name, created, progress))
 
            x = x + 1

def parsecl():
    usage = 'usage: %prog [options]'
    version = '%prog ' + VERSION
    description = "This program returns Snapshots for given Protection Group. Please contact ron@purestorage.com for any assistance."

    parser = OptionParser(usage=usage, version=version, description=description)

    parser.add_option('-d', '--debug',
                      type = 'int',
                      dest = 'DEBUG_LEVEL',
                      default = 0,
                      help = 'Debug level, used for HTTP debugging')
    
    parser.add_option('-l', '--limit',
                      type = 'int',
                      dest = 'limit',
                      default = 999,
                      help = 'Limit number of responses [default: %default]')
    
    parser.add_option('-p', '--password',
                      action = 'store',
                      type = 'string',
                      dest = 'password',
                      help = 'Pure password')
     
    parser.add_option('-q', '--quite',
                      action = 'store_true',
                      dest = 'QUITE_FLAG',
                      default = False,
                      help = 'Quite [default: %default]')
     
    parser.add_option('-P', '--pgroup',
                      action = 'store',
                      type = 'string',
                      dest = 'pgroup',
                      default = '',
                      help = 'Protection Group')
     
    parser.add_option('-s', '--server',
                      action = 'store',
                      type = 'string',
                      dest = 'flashArray',
                      help = 'Pure FlashArray')
        
    parser.add_option('-t', '--token',
                      action = 'store',
                      type = 'string',
                      dest = 'api_token',
                      help = 'Pure Api Token')

    parser.add_option('-u', '--user',
                      action = 'store',
                      type = 'string',
                      dest = 'user',
                      help = 'Pure user name')

    parser.add_option('-v', '--verbose',
                      action = 'store_true',
                      dest = 'VERBOSE_FLAG',
                      default = False,
                      help = 'Verbose [default: %default]')

    (options, args) = parser.parse_args()

    '''
    print("Options:", options)
    print("Args:", args)
    '''

    if options.api_token and options.user:
        parser.error('options --token and --user are mutually exclusive')
    
    return(options)

def main():
    # Setup variables
    global DEBUG_LEVEL
    global VERBOSE_FLAG
    global QUITE_FLAG
    exit_code = 0

    # Check for command line parameters
    options = parsecl()
    password = options.password
    user = options.user
    flashArray = options.flashArray
    limit = options.limit
    pgroup = options.pgroup
    api_token = options.api_token
    DEBUG_LEVEL = options.DEBUG_LEVEL
    VERBOSE_FLAG = options.VERBOSE_FLAG
    QUITE_FLAG = options.QUITE_FLAG
    
    if DEBUG_LEVEL != 0:
        print('Password', password)
        print('User', user)
        print('Flash Array', flashArray)
        print('Protection Group', pgroup)
        print('Limit', limit)
        print('Api Token', api_token)
        print('Debug Level:', DEBUG_LEVEL)
        print('Verbose Flag:', VERBOSE_FLAG)
        print('Quite Flag:', QUITE_FLAG)

    if flashArray == None:
        sys.exit('Exiting: You must provide FlashArray details')

    if api_token == None and user == None:
        sys.exit('Exiting: You must provide either API Token details or username and password')

    if user and password == None:
        sys.exit('Exiting: You must provide password if using username')

    if not QUITE_FLAG:
       print(BANNER)
       print(HEADER + ' - ' + flashArray)
       print(strftime('%d/%m/%Y %H:%M:%S %Z', gmtime()))
       print(BANNER)

    # Create session
    create_session(flashArray, user, password, api_token)

    list_pgsnaps(flashArray,pgroup,limit)
    
    if not QUITE_FLAG:
       print(BANNER)
       print(strftime('%d/%m/%Y %H:%M:%S %Z', gmtime()))
       print(BANNER)

    sys.exit(exit_code)

main()
