# Copyright (c) 2025, david-loe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, get_datetime, now_datetime

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

class Supporter(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from wohlfahrt_management.wohlfahrt_management.doctype.supporter_experience.supporter_experience import SupporterExperience
        from wohlfahrt_management.wohlfahrt_management.doctype.supporter_network.supporter_network import SupporterNetwork

        address_line_1: DF.Data | None
        address_line_2: DF.Data | None
        city: DF.Data | None
        contact_or_address_modified: DF.Data | None
        country: DF.Link | None
        date_of_birth: DF.Date | None
        email_address: DF.Data | None
        experiences: DF.Table[SupporterExperience]
        first_name: DF.Data | None
        full_name: DF.Data | None
        gender: DF.Link | None
        image: DF.AttachImage | None
        last_name: DF.Data | None
        networks: DF.Table[SupporterNetwork]
        phone: DF.Data | None
        postal_code: DF.Data | None
        salutation: DF.Link | None
    # end: auto-generated types

    # Felder, die für Adress- bzw. Kontaktdaten relevant sind
    address_fields = {"address_line_1", "city", "postal_code", "country"}
    contact_fields = {"address_line_2", "date_of_birth", "gender", "first_name", "last_name", "email_address", "phone", "salutation"}

    def has_fields_changed(self, fields: set, previous_doc: dict) -> bool:
        """
        Prüft, ob sich einer der angegebenen Felder im aktuellen Dokument im Vergleich zum vorherigen Dokument geändert hat.
        """
        return any(self.get(field) != previous_doc.get(field) for field in fields)

    def on_update(self) -> None:
        """
        Aktualisiert das Änderungsdatum für Kontakt- oder Adressdaten und löst bei Bedarf einen neuen Geocoding-Job aus.
        """
        # Lokales Flag: Bei neuen Dokumenten (__islocal == True) liegt bereits eine Änderung vor
        contact_or_address_modified = self.get("__islocal")

        # Hole das vorherige Dokument, falls vorhanden
        previous_doc = self.get_doc_before_save() or {}

        # Prüfe, ob alle erforderlichen Adressfelder gesetzt sind
        if all(self.get(field) for field in self.address_fields):
            # Falls ein vorheriges Dokument existiert, prüfe, ob sich die Adressfelder geändert haben
            if previous_doc:
                if not self.has_fields_changed(self.address_fields, previous_doc):
                    # Keine Änderung der Adressfelder: Kein Geocoding-Job erforderlich
                    return
                # Änderung festgestellt
                contact_or_address_modified = True
            # Starte neuen Geocoding-Job
            frappe.new_doc("Geocoding Job", supporter=self.name).insert(ignore_permissions=True)

        # Falls bislang noch keine Änderung festgestellt wurde, prüfe auch die Kontaktfelder
        if not contact_or_address_modified:
            if previous_doc and not self.has_fields_changed(self.address_fields.union(self.contact_fields), previous_doc):
                # Weder Adress- noch Kontaktfelder haben sich geändert
                return
            contact_or_address_modified = True

        # Aktualisiere das Änderungsdatum, falls nötig
        if contact_or_address_modified:
            # Aktualisiere das Feld nur, wenn es noch nicht gesetzt wurde oder sich nicht bereits dem aktuellen Zeitpunkt entspricht
            if (not self.contact_or_address_modified or 
                self.contact_or_address_modified == previous_doc.get("contact_or_address_modified")):
                self.contact_or_address_modified = now_datetime().strftime("%Y-%m-%d %H:%M:%S.%f")

    def validate(self) -> None:
        """
        Führt Validierungen vor dem Speichern des Dokuments durch, z. B. das Setzen des vollständigen Namens.
        """
        self.full_name = get_full_name(self.first_name, self.last_name)


def get_full_name(first_name: str, last_name: str) -> str:
    """
    Kombiniert Vor- und Nachname zu einem vollständigen Namen.
    """
    return " ".join(filter(None, [cstr(f).strip() for f in [first_name, last_name]]))
