from . import __version__ as app_version

app_name = "talleyapp1"
app_title = "Talleyapp"
app_publisher = "Ebuka"
app_description = "A simple application"
app_email = "ebukaakeru@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/talleyapp1/css/talleyapp1.css"
# app_include_js = "/assets/talleyapp1/js/talleyapp1.js"

# include js, css files in header of web template
# web_include_css = "/assets/talleyapp1/css/talleyapp1.css"
# web_include_js = "/assets/talleyapp1/js/talleyapp1.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "talleyapp1/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "talleyapp1.utils.jinja_methods",
#	"filters": "talleyapp1.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "talleyapp1.install.before_install"
# after_install = "talleyapp1.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "talleyapp1.uninstall.before_uninstall"
# after_uninstall = "talleyapp1.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "talleyapp1.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"talleyapp1.tasks.all"
#	],
#	"daily": [
#		"talleyapp1.tasks.daily"
#	],
#	"hourly": [
#		"talleyapp1.tasks.hourly"
#	],
#	"weekly": [
#		"talleyapp1.tasks.weekly"
#	],
#	"monthly": [
#		"talleyapp1.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "talleyapp1.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "talleyapp1.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "talleyapp1.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["talleyapp1.utils.before_request"]
# after_request = ["talleyapp1.utils.after_request"]

# Job Events
# ----------
# before_job = ["talleyapp1.utils.before_job"]
# after_job = ["talleyapp1.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"talleyapp1.auth.validate"
# ]
