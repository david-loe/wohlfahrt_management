import frappe
from frappe.utils.data import get_datetime
from wohlfahrt_management.wohlfahrt_management.doctype.supporter.supporter import DATE_TIME_FORMAT
from frappe.utils import update_progress_bar


def execute():
    """Set full name for all supporters"""
    frappe.db.auto_commit_on_many_writes = 1

    supporters = frappe.get_all(
        "Supporter",
        fields=["name", "modified"],
        filters={"contact_or_address_modified": ("is", "not set")},
        as_list=True,
    )
    total = len(supporters)
    for idx, (name, modified) in enumerate(supporters):
        update_progress_bar("Setting contact_or_address_modified for supporters", idx, total)
        frappe.db.set_value(
            "Supporter",
            name,
            "contact_or_address_modified",
            get_datetime(modified).strftime(DATE_TIME_FORMAT),
            update_modified=False,
        )

