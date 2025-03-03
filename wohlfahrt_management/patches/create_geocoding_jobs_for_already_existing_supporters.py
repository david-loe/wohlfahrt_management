import frappe


def execute():
    # Alle Supporter abrufen
    supporters = frappe.get_all(
        "Supporter",
        fields=["name", "address_line_1", "city", "postal_code", "country"],
        filters={"location": ("is", "not set")},
    )

    for supporter in supporters:
        # Prüfe, ob alle Adressfelder gesetzt sind
        if all(supporter.get(field) for field in ["address_line_1", "city", "postal_code", "country"]):
            # Optional: Prüfen, ob bereits ein Geocoding Job existiert
            if not frappe.db.exists("Geocoding Job", {"supporter": supporter.name}):
                frappe.new_doc("Geocoding Job", supporter=supporter.name).insert(ignore_permissions=True)
