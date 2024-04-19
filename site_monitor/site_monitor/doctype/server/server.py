# Copyright (c) 2024, Ebuka Akeru and contributors
# For license information, please see license.txt

# import frappe
import ipaddress,paramiko
from frappe.model.document import Document

import psutil 
 



class Server(Document):
    def fetch_server_cpu_metrics(self):
        """
            Fetch Some CPU Metrics linked to the server
        
        """
        import paramiko

    def fetch_server_metrics(self):
        try:
            # Create SSH client
            self.login_to_server()

            # Execute commands to fetch CPU-related information
            cpu_usage_command = "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1}'"
            cpu_load_average_command = "cat /proc/loadavg | awk '{print $1,$2,$3}'"
            interrupt_rate_command = "cat /proc/stat | grep 'intr'"

            stdin, stdout, stderr = self.client.exec_command(cpu_usage_command)
            cpu_usage = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command(cpu_load_average_command)
            cpu_load_average = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command(interrupt_rate_command)
            interrupt_rate = stdout.read().decode().strip()
            psutil_cpu_usage = psutil.cpu_percent()
            psutil_memory_usage = psutil.virtual_memory().percent  
            # Close the SSH connection
            self.client.close()

            return {
                "cpu_usage": cpu_usage,
                "cpu_load_average": cpu_load_average,
                "interrupt_rate": interrupt_rate,
                'psutil_cpu':psutil_cpu_usage,
                'psutil_mem':psutil_memory_usage
            }
        except paramiko.AuthenticationException:
            return "Authentication failed. Please check your username and password."
        except paramiko.SSHException as e:
            return f"SSH error: {e}"
        except Exception as e:
            return f"Error: {e}"

       

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


    