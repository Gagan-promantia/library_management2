# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryFeedback(Document):
	
	def on_submit(self):
		#After a feedback is submitted fetch other feedbacks for the same book
        #(respecting current user's permissions) and show the last 3 comments.

		if not self.book:
			return
		feedbacks=frappe.db.get_list(
			"Library Feedback",
			filters={"book":self.book},
			fields=["name","member","rating","comments","feedback_date"],
			order_by="creation desc",
			limit=3
		)

		formatted_feedbacks = "<br>".join(
        [f"{f['member']} ({f['rating']}/5): {f['comments']}" for f in feedbacks]
    )

		frappe.msgprint(f"Recent Feedbacks for this Book:<br>{formatted_feedbacks}")
		frappe.msgprint(f"Thank you for Recent feedbacks")

		# When an announcement is submitted, clear all old feedback records
		# frappe.db.truncate("Library Feedback")
		# frappe.db.commit()
		# frappe.msgprint("All old feedback records have been cleared.")

	def after_insert(self):
    # Get the rating value from database using frappe.db.get_value
		rating_value = frappe.db.get_value("Library Feedback", {"name": self.name}, "rating")

		if rating_value:
			frappe.msgprint(f"Your rating for this book is: <b>{rating_value}</b>")
		else:
			frappe.msgprint("Rating not found.")

		address=frappe.db.get_single_value("Library Single Doctype","library_branch")
		frappe.msgprint(f"You have given the feed back to {address} branch")
	    

		#deleting the where ratings is equal to 0
		frappe.db.delete("Library Feedback",{"rating":1})
		frappe.db.commit()
		frappe.msgprint("Feedbacks with 1 rating have been deleted.")
			
			
			#fetching the default currency of the system
		default_currency=frappe.db.get_default("curreny")
		if default_currency:
			frappe.msgprint(f"The system's default currency is: {default_currency}")
		else:
			frappe.msgprint("Default currency is not set.")

			#example of rollback if rating is too low
		try:
			if self.rating<=2:
				frappe.msgprint("Feedback ratingis low ! Rolling back")
				frappe.db.rollback()
				return 
			frappe.msgprint(f"Feeddback saved sucessfully with rating {self.rating}")

		except Exception as e:
			frappe.db.rollback()
			frappe.log_error(title="Feedback Rollback Error",message=str(e))
			frappe.throw("Something went wrong TRnascation rolled back")


	def before_insert(self):
	## Check if a feedback already exists for the same member and book
		# existing_feeback=frappe.db.exists(
		# 	"Library Feedback",
		# 	{
		# 		"member":self.member,
		# 		"book":self.book
		# 	}
		# )
		# if existing_feeback:
		# 	frappe.throw(f"A feedback already exists for this book and member (Feedback ID: {existing_feeback}")
		# else:
		# 	frappe.msgprint("No existing feedback found. Proceeding to create new one.")

    # Count total feedbacks given so far
		total_feedbacks = frappe.db.count("Library Feedback")

		# Count feedbacks given for the same book
		book_feedback_count = frappe.db.count("Library Feedback", {"book": self.book})

		frappe.msgprint(
			f"Total Feedbacks: {total_feedbacks}<br>"
			f"Feedbacks for this book: {book_feedback_count}"
		)
		
		
         #implementing the frappe.get_meta example
	def validate(Self):
		meta=frappe.get_meta("Library Feedback")
		field_list=[f.fieldname for f in meta.fields]
		frappe.msgprint(f"All fields in Library Feedback:{field_list}")
		
	
	