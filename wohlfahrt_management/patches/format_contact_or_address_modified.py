import frappe
from frappe.utils.data import get_datetime
from frappe.utils import update_progress_bar


def execute():
    """Format contact_or_address_modified for all supporters"""
    frappe.db.auto_commit_on_many_writes = 1

    supporters = frappe.get_all(
        "Supporter",
        fields=["name", "contact_or_address_modified"],
        filters={"contact_or_address_modified": ("is", "set")},
        as_list=True,
    )
    total = len(supporters)
    for idx, (name, contact_or_address_modified) in enumerate(supporters):
        update_progress_bar("Formatting contact_or_address_modified for supporters", idx, total)
        frappe.db.set_value(
            "Supporter",
            name,
            "contact_or_address_modified",
            get_datetime(contact_or_address_modified).isoformat(),
            update_modified=False,
        )

