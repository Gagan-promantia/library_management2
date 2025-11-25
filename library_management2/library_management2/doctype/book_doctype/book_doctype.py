# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookDoctype(Document):
	pass

# @frappe.whitelist()
# def get_book_info(book_title):
# 	book=frappe.db.get_value(
# 		"Book Doctype",
# 		{"book_title":book_title},
# 		["author","isbn", "shelf", "publisher", "publication_year", "description"],
# 		as_dict=True
# 	)
# 	if not book:
# 		return {"error":"Book not founf"}
# 	return book