# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class InvoiceDemo(Document):
	

	def before_naming(self):
		# Convert customer name to uppercase (example)
		if self.customer_name:
			self.customer_name = self.customer_name.upper()

		# Convert invoice_date (string) → date object
		if self.invoice_date:
			date_obj = getdate(self.invoice_date)
			self.invoice_year = date_obj.year

		print("before_naming executed")
