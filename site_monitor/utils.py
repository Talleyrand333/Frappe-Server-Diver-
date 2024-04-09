import frappe,json,requests
from frappe.utils import escape_html
from frappe.core.doctype.user.user import generate_keys


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
                return create_response(400,'User Already Registered',error )
                
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
            user.user_type = "Website User"
            user.flags.ignore_permissions = True
            user.flags.ignore_password_policy = True
            user.save()
            
            
            
            # set default signup role as per Portal Settings
            default_role = frappe.db.get_single_value("Portal Settings", "default_role")
            if default_role:
                user.add_roles(default_role)
            
            return create_response(200,'User Registered Successfully')
    except:
        frappe.log_error(title = "Error Creating New User",message = frappe.get_traceback())
        return create_response(500,"Error Creating New User",{})
    



def get_sites_servers(user):
    #Get the number of sites and servers the user created
    api_details = {}
    if not frappe.db.get_value("User",user,'api_key'):
        
        api_details = generate_keys(user)
        api_details['api_key'] = frappe.db.get_value("User",user,'api_key')
    else:
        
        user_doc = frappe.get_doc("User",user)
        api_details = {'api_key':user_doc.api_key,'api_secret':user_doc.get_password('api_secret')}
        
    api_details.update({'sites':0,'servers':0})
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
                return create_response(200,"Login Successful",user_dict )
            else:
                return create_response(200,"Login Successful",{'sites':sites,'servers':servers,'email':'johndoe@email.com','full_name':'John Doe'})
        else:
            raw_error = auth_api_response.content
            frappe.log_error(title = "Error Logging In",message = raw_error)
            return create_response(404,"Error Logging In")

    except Exception as error:
        frappe.log_error(title = "Error Logging In",message =error)
        return create_response(500,"Error Logging In")