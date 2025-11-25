import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class LibraryMembers(Document):
    @frappe.whitelist()
    def check_age(self):
        if self.age and self.age >= 18:
            return "Eligible for adult membership"
        else:
            return "Eligible for junior membership"
