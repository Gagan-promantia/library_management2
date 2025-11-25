# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.document import Document
from frappe.utils import nowdate, add_years

# class LibraryMember2(Document):
# 	def before_naming(self):
        
#         # Custom naming pattern before autoname()
        
# 		if self.member_type == "Student":
# 			self.name = f"STU-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"
# 		elif self.member_type == "Faculty":
# 			self.name = f"FAC-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"
# 		else:
# 			self.name = f"MEM-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"

# 		frappe.msgprint(f"Custom Name Set: {self.name}")

class LibraryMember2(Document):
    def autoname(self):
        frappe.logger().info(" before_naming() triggered for Library Member 2")

        if self.member_type == "Student":
            custom_name = f"STU-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"
        elif self.member_type == "Faculty":
            custom_name = f"FAC-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"
        else:
            custom_name = f"MEM-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"

        #  Assign name and mark it explicitly as custom
        self.name = custom_name
        self._localname = custom_name  # internal safeguard

    def before_insert(self):
        """Set default status and joining date before inserting a record."""
        if not self.joining_date:
            self.joining_date = frappe.utils.nowdate()

        # Set default status
        self.status = "Active"

    def db_insert(self, ignore_if_duplicate=False):
        """Custom logging of insertion process."""
        frappe.msgprint(f"🗃️ Inserting document into DB: {self.name}")

        # Important: call the original db_insert with the same argument
        super().db_insert(ignore_if_duplicate=ignore_if_duplicate)

        frappe.msgprint(f"Document {self.name} successfully inserted into database.")

    def after_insert(self):
        """Automatically create a default Membership record once a new member is added."""
        membership = frappe.get_doc({
            "doctype": "Library Membership2",
            "library_member": self.name,
            "from_date": nowdate(),
            "to_date": add_years(nowdate(), 1),
            "membership_type": "Standard",
            "status": "Active"
        })
        membership.insert(ignore_permissions=True)
        frappe.msgprint(f"Default 1-year membership created for {self.first_name}")

    
    def on_trash(self):
        # Prevent deleting a member with active issued books
        active_issues = frappe.db.exists("Library Transaction", {
            "member": self.name,
            "transaction_type": "Issue",
            "status": "Issued"
        })

        if active_issues:
            frappe.throw(f"Cannot delete member {self.name}: Active issued books exist.")

        frappe.msgprint(f" Member {self.name} deleted successfully.")

    def naming_rule(self):
        return "STU-.YYYY.-.####"