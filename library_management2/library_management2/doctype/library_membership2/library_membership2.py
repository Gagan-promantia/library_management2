# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMembership2(Document):
    def before_submit(self):
        # Ensure the membership has an expiry date before submission
        if not self.to_date:
            frappe.throw(" Cannot submit: Expiry Date (To Date) is mandatory before submission.")
        if self.status != "Active":
            frappe.throw(" Only Active memberships can be submitted.")
        
        frappe.msgprint("before_submit() executed successfully — validation passed.")
