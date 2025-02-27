# Copyright (c) 2025, david-loe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Supporter(Document):
    def on_update(self):
        # check if new geocoding job is needed
        fields = ["address_line_1", "city", "postal_code", "country"]
        if all(self.get(field) for field in fields):
            if not self.get("__islocal"):
                previous_doc = self.get_doc_before_save() or {}
                if not any(self.get(field) != previous_doc.get(field) for field in fields):
                    return
            frappe.new_doc("Geocoding Job", supporter=self.name).insert(ignore_permissions=True)
