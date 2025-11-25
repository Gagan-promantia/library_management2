# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

from io import BytesIO
import frappe
from frappe.website.website_generator import WebsiteGenerator


class LibraryBook2(WebsiteGenerator):
    # def after_insert(self):
    #     # Generate a QR code using the Book ID (name)
    #     qr = qrcode.make(self.name)

    #     # Save QR code into memory buffer
    #     buf = BytesIO()
    #     qr.save(buf, format='PNG')
    #     buf.seek(0)

    #     # Save the QR code image as a file attached to this document
    #     save_file(
    #         f"{self.name}_qrcode.png",
    #         buf.getvalue(),
    #         self.doctype,
    #         self.name,
    #         is_private=0
    #     )

    #     frappe.msgprint(f" QR Code generated and attached for book {self.name}")
	# def get_context(context):
    # # Access current document via context.doc
    #         book = context.doc
    #         # Example: show related books by same author
    #         context.related_books = frappe.get_all(
    #             "Library Book2",
    #             filters={"author": book.author, "name": ["!=", book.title]},
    #             fields=["title", "book_name", "route"]
    #         )
    #         return context
    pass
