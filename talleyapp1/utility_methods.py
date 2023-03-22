import frappe



def define_function():
    all_leaves = frappe.get_all("Employees")
    return all_leaves