import frappe

def execute(filters=None):
    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Data", "width": 300},
        {"label": "Type", "fieldname": "type", "fieldtype": "Data", "width": 120},
        {"label": "Parent", "fieldname": "parent", "fieldtype": "Data", "width": 200},
    ]

    data = []

    # ---- LEVEL 0: Library ----
    libraries = frappe.get_all("Library Doctype", fields=["name", "library_name"])
    for lib in libraries:
        data.append({
            "name": lib.library_name,
            "type": "Library",
            "parent": "",
            "indent": 0
        })

        # ---- LEVEL 1: Section ----
        sections = frappe.get_all(
            "Section Doctype",
            fields=["name", "section_name"],
            filters={"library": lib.name}
        )
        for section in sections:
            data.append({
                "name": section.section_name,
                "type": "Section",
                "parent": lib.library_name,
                "indent": 1
            })

            # ---- LEVEL 2: Shelf ----
            shelves = frappe.get_all(
                "Shelf Doctype",
                fields=["name", "shelf_name"],
                filters={"section": section.name}
            )
            for shelf in shelves:
                data.append({
                    "name": shelf.shelf_name,
                    "type": "Shelf",
                    "parent": section.section_name,
                    "indent": 2
                })

                # ---- LEVEL 3: Book ----
                books = frappe.get_all(
                    "Book Doctype",
                    fields=["name", "book_title"],
                    filters={"shelf": shelf.name}
                )
                for book in books:
                    data.append({
                        "name": book.book_title,
                        "type": "Book",
                        "parent": shelf.shelf_name,
                        "indent": 3
                    })

    return columns, data
