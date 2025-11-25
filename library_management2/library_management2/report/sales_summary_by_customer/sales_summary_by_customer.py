from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if filters is None:
		filters = {}

	user = frappe.session.user
	roles = frappe.get_roles(user)

	if "Test_role2" not in roles:
		frappe.throw("You don't have access to open this report.")

    # rest of your logic for data fetching
	columns = get_columns()
	data = get_data(filters)
	report_summary = get_report_summary(data)

	# Build a simple chart (sales amount per customer)
	chart = {
		"data": {
			"labels": [row.get("customer_name") for row in data],
			"datasets": [
				{"name": "Total Sales", "values": [row.get("total_sales") for row in data]}
			],
		},
		"type": "bar",
	}

	return columns, data, chart, report_summary


def get_columns():
	return [
		{"fieldname": "customer_name", "label": _("Customer"), "fieldtype": "Data", "width": 200},
		{"fieldname": "total_quantity", "label": _("Total Quantity"), "fieldtype": "Int", "width": 120},
		{"fieldname": "total_sales", "label": _("Total Sales"), "fieldtype": "Currency", "options": "currency", "width": 140},
		{"fieldname": "transactions", "label": _("Transactions"), "fieldtype": "Int", "width": 120},
		{"fieldname": "avg_sale", "label": _("Avg Sale Value"), "fieldtype": "Currency", "options": "currency", "width": 140},
	]


def get_data(filters):
	conditions = ["1=1"]
	values = {}

	if filters.get("from_date"):
		conditions.append("sr.sale_date >= %(from_date)s")
		values["from_date"] = filters.get("from_date")

	if filters.get("to_date"):
		conditions.append("sr.sale_date <= %(to_date)s")
		values["to_date"] = filters.get("to_date")

	if filters.get("status"):
		conditions.append("sr.status = %(status)s")
		values["status"] = filters.get("status")

	if filters.get("customer_name"):
		conditions.append("sr.customer_name = %(customer_name)s")
		values["customer_name"] = filters.get("customer_name")

	where = " AND ".join(conditions)  # ✅ fixed spacing here

	query = f"""
		SELECT
			sr.customer_name AS customer_name,
			SUM(COALESCE(sr.quantity, 0)) AS total_quantity,
			SUM(COALESCE(sr.quantity * sr.price, COALESCE(sr.total, 0))) AS total_sales,
			COUNT(*) AS transactions,
			CASE WHEN SUM(COALESCE(sr.quantity, 0)) = 0 THEN 0
				ELSE ROUND(SUM(COALESCE(sr.quantity * sr.price, COALESCE(sr.total, 0))) / SUM(COALESCE(sr.quantity, 0)), 2)
			END AS avg_sale
		FROM `tabSales Record` sr
		WHERE {where}
		GROUP BY sr.customer_name
		ORDER BY total_sales DESC
	"""

	rows = frappe.db.sql(query, values=values, as_dict=True)

	for r in rows:
		r["total_quantity"] = int(r.get("total_quantity") or 0)
		r["transactions"] = int(r.get("transactions") or 0)

	return rows


def get_report_summary(data):
	total_sales = sum([r.get("total_sales") or 0 for r in data])
	total_qty = sum([r.get("total_quantity") or 0 for r in data])
	return [
		{"value": total_sales, "indicator": "Green", "label": _("Total Sales"), "datatype": "Currency", "currency": "INR"},
		{"value": total_qty, "indicator": "Blue", "label": _("Total Quantity"), "datatype": "Int"},
	]
