app_name = "wohlfahrt_management"
app_title = "Wohlfahrt Management"
app_publisher = "david-loe"
app_description = "Effiziente Verwaltung von Wohlfahrtsorganisation und Unterstützern"
app_email = "kontakt@david-loe.de"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "wohlfahrt_management",
# 		"logo": "/assets/wohlfahrt_management/logo.png",
# 		"title": "Wohlfahrt Management",
# 		"route": "/wohlfahrt_management",
# 		"has_permission": "wohlfahrt_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/wohlfahrt_management/css/wohlfahrt_management.css"
# app_include_js = "/assets/wohlfahrt_management/js/wohlfahrt_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/wohlfahrt_management/css/wohlfahrt_management.css"
# web_include_js = "/assets/wohlfahrt_management/js/wohlfahrt_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "wohlfahrt_management/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "wohlfahrt_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "wohlfahrt_management.utils.jinja_methods",
# 	"filters": "wohlfahrt_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "wohlfahrt_management.install.before_install"
# after_install = "wohlfahrt_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "wohlfahrt_management.uninstall.before_uninstall"
# after_uninstall = "wohlfahrt_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "wohlfahrt_management.utils.before_app_install"
# after_app_install = "wohlfahrt_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "wohlfahrt_management.utils.before_app_uninstall"
# after_app_uninstall = "wohlfahrt_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wohlfahrt_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "hourly_long": ["wohlfahrt_management.geocoding_queue.process_geocoding_queue"],
    "daily": ["wohlfahrt_management.geocoding_queue.delete_successfull_jobs_older_than_1_week"],
}

# Testing
# -------

# before_tests = "wohlfahrt_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "wohlfahrt_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "wohlfahrt_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["wohlfahrt_management.utils.before_request"]
# after_request = ["wohlfahrt_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["wohlfahrt_management.utils.before_job"]
# after_job = ["wohlfahrt_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"wohlfahrt_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
