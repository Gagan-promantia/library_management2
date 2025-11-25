# apps/library_management2/library_management2/report/student_enrollment_summary/student_enrollment_summary.py
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    if filters is None:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    # Optional: a simple summary
    total_enrollments = len(data)
    report_summary = [{
        "value": total_enrollments,
        "indicator": "Blue",
        "label": _("Total Enrollments"),
        "datatype": "Int"
    }]

    # return columns, data (optionally chart, report_summary, skip_total_rows)
    return columns, data, None, report_summary

def get_columns():
    return [
        {"fieldname": "student", "label": _("Student"), "fieldtype": "Link", "options": "Student", "width": 200},
        {"fieldname": "course", "label": _("Course"), "fieldtype": "Link", "options": "Course", "width": 200},
        {"fieldname": "enrollment_date", "label": _("Enrollment Date"), "fieldtype": "Date", "width": 110},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 90},
        {"fieldname": "duration", "label": _("Duration (days)"), "fieldtype": "Int", "width": 120},
        {"fieldname": "fees", "label": _("Fees"), "fieldtype": "Currency", "options": "currency", "width": 120}
    ]

def get_data(filters):
    # Build SQL with filters for efficiency (or use frappe.get_all)
    conditions = []
    values = {}

    if filters.get("student"):
        conditions.append("ce.student = %(student)s")
        values["student"] = filters.get("student")
    if filters.get("course"):
        conditions.append("ce.course = %(course)s")
        values["course"] = filters.get("course")
    if filters.get("from_date"):
        conditions.append("ce.enrollment_date >= %(from_date)s")
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions.append("ce.enrollment_date <= %(to_date)s")
        values["to_date"] = filters.get("to_date")
    if filters.get("status"):
        conditions.append("ce.status = %(status)s")
        values["status"] = filters.get("status")

    where = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            ce.student AS student,
            ce.course AS course,
            ce.enrollment_date AS enrollment_date,
            ce.status AS status,
            DATEDIFF(COALESCE(ce.end_date, CURDATE()), ce.enrollment_date) AS duration,
            ce.fees AS fees
        FROM `tabCourse Enrollment` ce
        WHERE {where}
        ORDER BY ce.enrollment_date DESC
    """

    rows = frappe.db.sql(query, values=values, as_dict=True)
    # Convert results into list of dicts exactly matching columns' fieldnames
    return rows
