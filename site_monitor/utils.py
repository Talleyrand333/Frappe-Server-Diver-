import frappe,json,requests
from frappe.utils import escape_html,getdate
from frappe.utils.user import add_role
import socket
import ssl
import datetime

test124= "HEADERS"


def has_default_role(user):
    roles = frappe.get_roles(user)
    default_role = frappe.get_value("General Settings",None,'base_role_for_user')
    if not default_role:
        return False
    if default_role in roles:
        return True
    return False

def get_url_details(url):
    #Return a dictionary of IP address, SSL status and number of days till expiry
    encryption_status = "No"
    days_until_expiry = 0
    expiry_date = getdate()
    try:
        ip = socket.gethostbyname(url)
        
    except:
        ip = None
        frappe.log_error(title = "Error fetching IP Address",message = frappe.get_traceback())
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url) as s:
            s.settimeout(3)  # Adjust timeout as needed
            s.connect((url, 443))
            ssl_info = s.getpeercert()
            encryption_status = "Yes"
            expires_on = datetime.datetime.strptime(ssl_info['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_until_expiry = (expires_on - datetime.datetime.now()).days
            expiry_date = getdate(expires_on)
            return {'expiry_date':expiry_date,'ip':ip,'encryption_status':encryption_status,'days_until_expiry':days_until_expiry}
    except ssl.SSLError:
        encryption_status = "No"
        days_until_expiry = 0
        return {'expiry_date':expiry_date,'ip':ip,'encryption_status':encryption_status,'days_until_expiry':days_until_expiry}
    except socket.timeout:
        frappe.log_error(title="Socket Timeout",message = frappe.get_traceback())
        return {'expiry_date':expiry_date,'ip':ip,'encryption_status':encryption_status,'days_until_expiry':days_until_expiry}
    except Exception as e:
        frappe.log_error(title="Error Validating Site Encryption",message = frappe.get_traceback())
        return {'expiry_date':expiry_date,'ip':ip,'encryption_status':encryption_status,'days_until_expiry':days_until_expiry}
    
    
@frappe.whitelist()
def create_new_site(recipient,url,username):
    try:
        if not has_default_role(username):
            userdoc = frappe.get_doc('User',username)
            add_role_to_user(userdoc = userdoc)
            frappe.db.commit() 
        if not recipient:
            create_response(400,"Please set a recipient",None)
        if not url:
            create_response(400,"Please set a URL",None)
        
        url = str(url) #just incase
        if not url.startswith('http') and not url.startswith('https'):
            if url.startswith('www.'):
                url = 'http://'+url
            else:
                create_response(400,"Please Set URL in either www.,https:// or http:// format",None)
            #No need to do anything
        site_details = get_url_details(url)
        new_site = frappe.new_doc("Site")
        new_site.url = url
        new_site.notification_recipient = recipient
        new_site.site_owner = username
        new_site.server_ip = site_details.get('ip')
        new_site.ssl_installed =  site_details.get('encryption_status')
        new_site.days_till_ssl_expiry = site_details.get("days_until_expiry")
        new_site.expiry_date    = site_details.get('expiry_date')
        new_site.save()
        
        return create_response(201,"Site Created Successfully",data = {'url':url,'recipient':recipient}.update(site_details))
    except:
        frappe.log_error(title="Error Creating Site",message = frappe.get_traceback())
        
        # return create_response(500,"An Error Occured",None)
        return create_response(500,frappe.get_traceback(),None)
    
    
def generate_user_keys(user):
	"""
	generate api key and api secret

	:param user: str
	"""
	
	user_details = frappe.get_doc("User", user)
	api_secret = frappe.generate_hash(length=15)
	# if api key is not set generate api key
	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
	user_details.api_secret = api_secret
	user_details.save()

	return {"api_secret": api_secret}

def create_response(status,message,data=None):
    #Create a standard reponse method
    
    response_data = {
        'status':status,
        'message':message,
        'data':data
    }
    
    response = json.dumps(response_data)
    return response


@frappe.whitelist(allow_guest=True)
def create_new_user(email, full_name, password):
    try:
        
        user = frappe.db.get("User", {"email": email})
        
        if user:
            
            if user.enabled:
                
                return create_response(400,'User Already Registered',{} )
                
            else:
                
                return create_response(400,'User Registered but disabled')
                
        else:
            if frappe.db.get_creation_count("User", 60) > 300:
                return create_response(429,"Too many users signed up recently, so the registration is disabled. Please try back in an hour")
            
            
            user = frappe.new_doc("User")
            user.email = email
            user.first_name =  escape_html(full_name)
            user.enabled = 1
            user.new_password = password
            user.user_type = "System User"
            user.flags.ignore_permissions = True
            user.flags.ignore_password_policy = True
            # set default signup role as per Portal Settings
            default_role = frappe.db.get_single_value("General Settings", "base_role_for_user")
            if default_role:
                user.add_roles(default_role)
            return create_response(200,'User Registered Successfully')
    except:
        frappe.log_error(title = "Error Creating New User",message = frappe.get_traceback())
        
        return create_response(500,"Error Creating New User",{})
    


def add_role_to_user(userstring = None, userdoc = None):
    #add the default server diver role to all users that register and login through the API and do not have the role
    try:
        default_role = frappe.db.get_single_value("General Settings", "base_role_for_user")
        if default_role:
            if not userdoc:
                userdoc = frappe.get_doc("User",userstring)
            userdoc.user_type= "System User"
            current_roles = [d.role for d in userdoc.get("roles")]
            if default_role in current_roles:
                return
            userdoc.append("roles", {"role": default_role})
            userdoc.flags.ignore_permissions = 1
            userdoc.save()
           
    except:
        frappe.log_error(title = 'Error Attaching Role',message = frappe.get_traceback())
        
def get_users_sites_servers(user):
    """
    Return a dictionary of the number of sites and servers created by that user currently being monitored
    """
    sites,servers = 0,0
    sites = frappe.db.count('Site', {'site_owner':user})
    return {'sites':sites,'servers':servers}
    
def get_sites_servers(user):
    #Get the number of sites and servers the user created
    api_details = {}
    sites_servers = get_users_sites_servers(user)
    if not frappe.db.get_value("User",user,'api_key'):
        frappe.session.user = "Administrator"
        api_details = generate_user_keys(user)
        api_details['api_key'] = frappe.db.get_value("User",user,'api_key')
    else:
        
        user_doc = frappe.get_doc("User",user)
        api_details = {'api_key':user_doc.api_key,'api_secret':user_doc.get_password('api_secret')}
        
    api_details.update({'sites':sites_servers.get('sites'),'servers':sites_servers.get('servers')})
    return api_details

    
@frappe.whitelist(allow_guest=True)
def login(username: str = None, password: str = None) -> dict:
    """ This method logs in the user provided appropriate paramaters.

    Args:
        
        username (str): Email Id of user
        password (str): Erpnext Password

    Returns:
        response (dict): {
            message (str): Brief message indicating the response.
            data (dict): { 
                api_token (str), 			
                token_type (str) -> "token", 
                full_name (str), 
                email_address (str), 
                image (str), 
                sites int), 
                servers (int)
            }
        }
    """
    
    
    if not username:
        return create_response(400, "Username is required!",None)
    
    if not password:
        return create_response(400, "Password is required!",None)

    if not isinstance(username, str):
        return create_response(400, "Username must be a string!",None)

    if not isinstance(password, str):
        return create_response(400, "Password must be a string!",None)

    
    try:
        site = frappe.utils.get_url()+'/'
        username_exists =  frappe.db.exists("User", {'name': username})

        if not username_exists:
            return create_response(401, "Invalid Username",None)
        
        args = {
            'usr': username,
            'pwd': password
        }
        headers = {'Accept': 'application/json'}
        session = requests.Session()
        auth_api = site + "api/method/login"
        auth_api_response = session.post(
            auth_api,
            data=args, headers=headers
        )

        if auth_api_response.status_code == 200:
            
            
            #Get Number of sites,servers for user
            user_server_details = get_sites_servers(username)
            user_dict = json.loads(auth_api_response.content)
            if user_dict:	
                user_dict.update(user_server_details)
                if not has_default_role(username):
                    add_role_to_user(userstring = username)
                return create_response(200,"Login Successful",user_dict )
            else:
                return create_response(200,"Login Successful",{'sites':sites,'servers':servers,'email':'johndoe@email.com','full_name':'John Doe'})
        else:
            frappe.log_error(title="Issue Logging In",message = auth_api_response)
            raw_error = auth_api_response.content
            frappe.log_error(title = "Error Logging In",message = raw_error)
            return create_response(404,"Invalid Login Credentials")

    except Exception as error:
        
        frappe.log_error(title = "Error Logging In",message =frappe.get_traceback())
        return create_response(500,"Error Logging In")