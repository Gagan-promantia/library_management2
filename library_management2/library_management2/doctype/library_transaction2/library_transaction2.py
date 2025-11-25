# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, nowdate, add_days, getdate
from frappe.utils import now_datetime


class LibraryTransaction2(Document):
    def before_validate(self):
        # Ensure the selected book is available before issuing.
        # fetch book details
        book_status = frappe.db.get_value("Library Book2", self.book, "book_status")
        if self.transaction_type == "Issue" and book_status != "Available":
            frappe.throw(f"The book '{self.book}' is currently not available!")
        if self.transaction_type == "Issue" and not self.issue_date:
            self.issue_date = nowdate()

    def validate(self):
        if not self.due_date:
            base_date = self.issue_date or nowdate()
            self.due_date = add_days(base_date, 14)
            self.db_set("due_date", self.due_date)
        if self.transaction_type == "Issue" and getdate(self.due_date) < getdate(self.issue_date):
            frappe.throw("Due date must be after the issue date.")

    def before_save(self):
        # Ensure due_date exists, then calculate fine
        if not self.due_date and self.issue_date:
            self.due_date = add_days(self.issue_date, 14)
            self.db_set("due_date", self.due_date)

        self.calculate_fine()

    def on_submit(self):
        if self.book:
            # Get the linked Library Book2 document
            book_doc = frappe.get_doc("Library Book2", self.book)
            if self.status == "Issued":
                # Reduce available copies
                book_doc.available_copies -= 1
                book_doc.save()
                frappe.msgprint(f" Book '{book_doc.title}' issued. Remaining copies: {book_doc.available_copies}")

    def on_cancel(self):
        if self.book:
            # Get the linked Library Book2 document
            book_doc = frappe.get_doc("Library Book2", self.book)
            if self.status == "Issued":
                # Add the copy back
                book_doc.available_copies += 1
                book_doc.save()
                frappe.msgprint(f" Transaction cancelled — '{book_doc.title}' restored. Copies: {book_doc.available_copies}")

    def calculate_fine(self):
        if self.return_date and self.due_date and getdate(self.return_date) > getdate(self.due_date):
            days_late = (getdate(self.return_date) - getdate(self.due_date)).days
            self.fine_amount = days_late * 5
        else:
            self.fine_amount = 0

    def before_cancel(self):
        """Check before allowing cancellation of a Library Transaction."""
        # Example 1: Prevent cancel if fine is still unpaid
        if self.fine_amount and self.fine_amount > 0:
            frappe.throw(f" Cannot cancel this transaction! Fine amount of ₹{self.fine_amount} must be settled first.")
        
        # Example 2: Ensure status isn't already marked 'Returned'
        if self.status == "Returned":
            frappe.throw(" Cannot cancel a transaction where the book is already returned.")
        
        frappe.msgprint(" before_cancel() check passed — proceeding to cancellation.")

    def before_update_after_submit(self):
        # Fetch the existing submitted version from the database
        old_doc = frappe.get_doc(self.doctype, self.name)

        # Compare the member field
        if old_doc.member != self.member:
            frappe.throw("You cannot change the Member field after submission.")

    def on_trash(self):
        # frappe.logger().info(f"Book '{self.name}' deleted by user '{frappe.session.user}'")
        # frappe.msgprint(f"Book {self.title} deleted by {frappe.session.user}")
        if self.status != "Returned":
            frappe.throw("You cannot delete a transaction until the book is returned.")



    def on_update(self):
        self.last_activity = now_datetime()
        frappe.msgprint(f" Last activity updated to {self.last_activity}")

    def on_change(self):
        # Automatically set status based on transaction type selection
        if self.transaction_type == "Issue":
            self.status = "Issued"
        elif self.transaction_type == "Return":
            self.status = "Returned"

   
    def before_submit(self):
    # Check if the book is available
        if self.book and self.book.available_copies <= 0:
            frappe.throw(f"Book '{self.book}' is not available for issue.")

    def on_update_after_submit(self):
        if self.status == "Returned":
            # Fetch book and increase available copies
            book = frappe.get_doc("Library Book", self.book)
            book.available_copies += 1
            book.save()
            frappe.msgprint(f"Book '{book.name}' has been returned and stock updated.")