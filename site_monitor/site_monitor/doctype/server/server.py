# Copyright (c) 2024, Ebuka Akeru and contributors
# For license information, please see license.txt

# import frappe
import ipaddress,paramiko
from frappe.model.document import Document

import psutil 
 



class Server(Document):
    def validate(self):
        if self.is_new():
            server_data = self.fetch_server_metrics()
            self.update(server_data)
            
    def fetch_server_cpu_metrics(self):
        """
            Fetch Some CPU Metrics linked to the server
        
        """
        import paramiko
        
    
    def fetch_server_metrics(self):
        try:
            # Create SSH client
            logged_in = False
            self.login_to_server()
            logged_in = True
            # Use shell commands for memory and swap info
            stdin, stdout, stderr = self.client.exec_command("free -b")
            memory_info_output = stdout.read().decode().strip().splitlines()[1:]

            # Parse memory info
            mem_tag,total_mem, used_mem, free_mem,shared, buffers, available = memory_info_output[0].split()

            # Swap space info
            stdin, stdout, stderr = self.client.exec_command("swapon -s")
            swap_info_output = stdout.read().decode().strip().splitlines()

            swap_usage = None  # Initialize swap usage

            if len(swap_info_output) > 1:  # Check if swap is enabled
                swap_info = swap_info_output[1].split()
                swap_total = swap_info[2]
                swap_used = swap_info[3]
                swap_free = swap_info[4]

                # Calculate swap usage percentage
                swap_usage = float(swap_used) / float(swap_total) * 100

            # Use psutil for CPU usage
            psutil_cpu_usage = psutil.cpu_percent()

            # CPU load average
            cpu_load_average = psutil.getloadavg()[0]  # Get 1-minute load average

            # Interrupt rate
            stdin, stdout, stderr = self.client.exec_command("cat /proc/stat | grep 'intr'")
            interrupt_rate = stdout.read().decode().strip()

            # Close SSH connection
            self.client.close()
            total_mem =  int(total_mem) / (1024**3) # Convert to GB
            free_mem = int(free_mem) / (1024**3)
            used_memory = int(used_mem) / (1024**3),
            return {
                "cpu_usage_percent": psutil_cpu_usage,
                "cpu_load_average": cpu_load_average,
                "total_memory": total_mem,  
                "free_memory": free_mem,
                "used_memory":used_memory,
                "memory_utilization":(free_mem/total_mem)*100,
                "buffer_cache": int(buffers) / (1024**3),
                "available": int(available) / (1024**3),
                "swap_usage": swap_usage,
            }
            # ... (error handling)
        except:
            if logged_in:
                self.client.close()
            frappe.log_error(title= "Error Fetching Server Data",message = frappe.get_traceback())
        
       

    def validate_server_ip(self):
        "Confirm that the IP provided is publicly accessible"
        try:
            ipaddress.ip_interface(self.server_ip)
            return True
        except (ValueError, ipaddress.AddressValueError):
            return False
    
    def login_to_server(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        self.client.connect(hostname=self.server_ip.strip(), username=self.server_username,password = self.get_password('server_password'),allow_agent=False, look_for_keys=False)
    
    def autoname(self):
        if self.server_ip and self.server_username:
            if self.validate_server_ip():
                self.name =  f"{self.server_username}@{self.server_ip}"
            else:
                frappe.throw(f"Oh Oh, It seems <b>{self.server_ip}</b> is not a valid IP")


    