# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class LibraryTransaction3(Document):
	pass
	# def after_insert(self):
    #     # Get today's date
	# 	current_date = today()

    #     # Run SQL query to find transactions created today
	# 	transactions = frappe.db.sql("""
    #         SELECT student_name, transaction_date
    #         FROM `tabLibrary Transaction3`
    #         WHERE transaction_date = %s
    #     """, (current_date,), as_dict=True)

    #     # Show result count in a message
	# 	frappe.msgprint(f"Found {len(transactions)} transaction(s) with today's date: {current_date}")

    #     # Optional: Show details
	# 	for t in transactions:
	# 		frappe.msgprint(f"Transaction: {t.name}, Student_name: {t.student_name}, Date: {t.transaction_date}")
		

	# 	records = frappe.db.multisql({
    # 	"mariadb": """
    #     SELECT name, student_name, transaction_date, status
    #     FROM `tabLibrary Transaction3`
    #     WHERE status = %s
   	# 		 """,
    # 	"postgres": """
    #     SELECT name, student_name, transaction_date, status
    #     FROM "tabLibrary Transaction3"
    #     WHERE status = $1
   	# 	 """,
	# 	}, ("Borrowed",), as_dict=True)

	# 	frappe.msgprint(str(records))

	# # def before_save(self):
    # # 			frappe.throw("This student name is not allowed!")
	# #this is for frappe.call
	# # @frappe.whitelist()
	# # def describe_transaction_table():
	# # 	description = frappe.db.describe("tabLibrary Transaction3")
	# # 	frappe.msgprint(str(description))


	# # def after_insert(self):
    # #     # Corrected table name
	# # 	frappe.db.change_column_type("tabLibrary Transaction3", "student_name", "TEXT")
	# # 	frappe.msgprint("Column type changed to TEXT successfully!")


	# # def after_insert(self):
    # #     # Add an index on the student_name column
	# # 	frappe.db.add_index("Library Transaction3", "idx_student_name", ["student_name"])
	# # 	frappe.msgprint("Index added successfully on student_name!")

	# def after_insert(self):
    #     # Imagine this method uploads a file
	# 	self.create_file()

	# def create_file(self):
    #     # Example: simulate writing file to disk
	# 	self.file_path = "/tmp/student_" + self.name + ".txt"
	# 	with open(self.file_path, "w") as f:
	# 		f.write("This is a test file for " + self.student_name)

	# 		frappe.msgprint("File created successfully: " + self.file_path)

    #     # If DB transaction fails and rolls back → delete file
	# 	frappe.db.after_rollback.add(self.rollback_file)

    #     # If commit succeeds → confirm final message
	# 	frappe.db.after_commit.add(self.commit_file)

	# def rollback_file(self):
	# 	import os
	# 	if os.path.exists(self.file_path):
	# 		os.remove(self.file_path)
	# 		frappe.msgprint("File deleted because transaction was rolled back.")

	# def commit_file(self):
	# 	frappe.msgprint("Transaction committed successfully, file kept.")


	# def before_save(self):
    #     # Normal save process
	# 	frappe.msgprint(f"Attempting to save transaction for: {self.student_name}")

    #     # Artificial validation to cause rollback
	# 	if self.student_name == "Test Error":
	# 		frappe.throw("Invalid student name! Rolling back the transaction.")
        
	# 	frappe.msgprint("Transaction will be saved successfully if no error occurs.")

@frappe.whitelist()
#add self inside method if calling directly
def describe_transaction_table():
	description = frappe.db.describe("Library Transaction3")
	frappe.msgprint(str(description))