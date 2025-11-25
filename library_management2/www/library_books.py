import frappe


def get_context(context):
    books = frappe.get_all(
        "Library Book2",
        fields=["title", "author", "isbn"],
        filters={"is_published": 1},
        order_by="creation desc"
    )
    context.books = books
    context.title = "Library Books"
    return context
