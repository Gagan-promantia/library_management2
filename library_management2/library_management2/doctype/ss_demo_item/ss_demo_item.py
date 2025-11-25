# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SSDemoItem(Document):
	def after_insert(self):
        # Replace this string with the EXACT DocType Name of your log
		LOG_DOCTYPE = "SS Demo Log"   # <-- check spelling in your UI

		log = frappe.new_doc(LOG_DOCTYPE)
		log.item = self.name
		log.note = f"Created from after_insert for {self.item_name}"
		log.insert(ignore_permissions=True)
		frappe.db.commit()