import json
import time
import requests, frappe


def check_if_new_geocoding_job_is_needed(doc, method):
    fields = ["address_line_1", "city", "postal_code", "country"]

    if not all(doc.get(field) for field in fields):
        return

    if doc.get("__islocal"):
        frappe.new_doc("Geocoding Job", supporter=doc.name).insert(ignore_permissions=True)
        return

    previous_doc = doc.get_doc_before_save() or {}

    if any(doc.get(field) != previous_doc.get(field) for field in fields):
        frappe.new_doc("Geocoding Job", supporter=doc.name).insert(ignore_permissions=True)


def process_geocoding_queue():
    settings = frappe.get_single("Geocoding API Settings")
    if settings.url:
        jobs = frappe.get_all("Geocoding Job", filters={"status": "Pending"}, limit_page_length=0)
        for job in jobs:
            job_doc = frappe.get_doc("Geocoding Job", job.name)
            supporter_doc = frappe.get_doc("Supporter", job_doc.supporter)
            if not supporter_doc:
                job_doc.update({"status": "Failed", "error_message": "Supporter not found"})
                job_doc.save()
                continue

            address_data = {
                "address_line_1": supporter_doc.address_line_1,
                "address_line_2": supporter_doc.address_line_2,
                "city": supporter_doc.city,
                "postal_code": supporter_doc.postal_code,
                "country": supporter_doc.country,
            }

            api_url = frappe.render_template(settings.url, address_data)

            try:
                app_name = frappe.get_hooks("app_name")[0]
                app_version = frappe.get_hooks("app_version")[0]
                site_url = frappe.utils.get_url()
                headers = {"User-Agent": f"{app_name}/{app_version} (+{site_url})", "Referer": site_url}
                if settings.headers:
                    headers.update(frappe.parse_json(settings.headers))

                response = requests.get(api_url, headers=headers)

                response.raise_for_status()
                data = response.json()

                lat = get_nested_value(data, settings.lat_param)
                lon = get_nested_value(data, settings.lon_param)
                if lat is None or lon is None:
                    raise ValueError(f"Coordinates could not be extracted from the response: {data}")
                if isinstance(lat, str):
                    lat = float(lat)
                if isinstance(lon, str):
                    lon = float(lon)
                geojson = json.dumps(
                    {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {},
                                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                            }
                        ],
                    }
                )

                supporter_doc.db_set("location", geojson, update_modified=False, commit=True, notify=True)

                job_doc.status = "Completed"
            except Exception as e:
                job_doc.update({"status": "Failed", "error_message": str(e)})
                frappe.log_error(message=str(e), title="Geocoding Fehler")
            job_doc.save()
            frappe.db.commit()
            if settings.req_interval_ms > 0:
                time.sleep(settings.req_interval_ms / 1000.0)


def get_nested_value(data, key_path):
    """
    Extrahiert einen Wert aus einem verschachtelten JSON-Dictionary oder einer Liste anhand eines
    dot-notation Pfads (z. B. "result.location.lat" oder "results.0.lat").
    """
    for key in key_path.split("."):
        if isinstance(data, list):
            try:
                index = int(key)
                data = data[index]
                continue
            except (ValueError, IndexError):
                return None

        if isinstance(data, dict):
            if key in data:
                data = data[key]
            else:
                return None
        else:
            return None
    return data
