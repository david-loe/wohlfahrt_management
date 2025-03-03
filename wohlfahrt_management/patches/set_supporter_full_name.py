import frappe
from wohlfahrt_management.wohlfahrt_management.doctype.supporter.supporter import get_full_name
from frappe.utils import update_progress_bar


def execute():
    """Set full name for all supporters"""
    frappe.db.auto_commit_on_many_writes = 1

    supporters = frappe.get_all(
        "Supporter",
        fields=["name", "first_name", "last_name"],
        filters={"full_name": ("is", "not set")},
        as_list=True,
    )
    total = len(supporters)
    for idx, (name, first, last) in enumerate(supporters):
        update_progress_bar("Setting full name for supporters", idx, total)
        try:
            frappe.db.set_value(
                "Supporter",
                name,
                "full_name",
                get_full_name(first, last),
                update_modified=False,
            )
        except frappe.db.DataError as e:
            if frappe.db.is_data_too_long(e):
                print("Full name is too long for DB column, skipping")
                continue
            raise e
