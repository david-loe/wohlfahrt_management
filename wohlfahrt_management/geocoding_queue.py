import time
import frappe


def process_geocoding_queue():
    settings = frappe.get_single("Geocoding API Settings")
    if settings.url:
        jobs = frappe.get_all("Geocoding Job", filters={"status": "Pending"})
        for job in jobs:
            job_doc = frappe.get_doc("Geocoding Job", job.name)
            job_doc.run(settings)
            if settings.req_interval_ms > 0:
                time.sleep(settings.req_interval_ms / 1000.0)


def delete_successfull_jobs_older_than_1_week():
    frappe.db.sql(
        """
        DELETE FROM `tabGeocoding Job`
        WHERE status = 'Successfull'
        AND modified < DATE_SUB(NOW(), INTERVAL 1 WEEK)
        """
    )
