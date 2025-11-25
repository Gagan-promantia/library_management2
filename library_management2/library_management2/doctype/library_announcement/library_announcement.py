import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from frappe.model.mapper import get_mapped_doc
from frappe.utils import (
    nowdate, add_days, date_diff, random_string, flt, cint, strip_html_tags
)

class LibraryAnnouncement(Document):

    @frappe.whitelist()
    # def create_announcement(self,title, message, priority="Medium", posted_by="System"):
    #     doc = frappe.new_doc("Library Announcement")
    #     doc.title = title
    #     doc.message = message
    #     doc.date = nowdate()
    #     doc.priority = priority
    #     doc.posted_by = posted_by
    #     doc.insert()
    #     frappe.db.commit()
    #     return f"✅ Announcement created successfully with name: {doc.name}"

    def get_all_announcements():
        """Return all announcements with key details."""
        data = frappe.db.get_all(        #it will give in dictionary format
            "Library Announcement",
            fields=["name", "title", "message", "date", "priority", "posted_by"],
            order_by="creation desc"
        )
        return data

    def get_announcement(name):
        """Fetch a specific announcement by name."""
        doc = frappe.get_cached_doc("Library Announcement", name)  #get_doc also does same job ,, with less performance
        return {
            "title": doc.title,
            "message": doc.message,
            "priority": doc.priority,
            "date": doc.date,
            "posted_by": doc.posted_by
        }

    def get_last_announcement():
        """Get the last created Library Announcement."""
        last_doc = frappe.get_last_doc("Library Announcement")
        return {
            "name": last_doc.name,
            "title": last_doc.title,
            "priority": last_doc.priority,
            "posted_by": last_doc.posted_by,
            "date": last_doc.date
        }

    def get_announcement2(name):
        """Fetch a specific announcement by name."""
        doc = frappe.get_cached_doc("Library Announcement", name)
        return {
            "title": doc.title,
            "message": doc.message,
            "priority": doc.priority,
            "date": doc.date,
            "posted_by": doc.posted_by
        }

    def map_announcement_to_copy(source_name):
        """Map a Library Announcement to Library Announcement2"""
        target_doc = get_mapped_doc(
            "Library Announcement",
            source_name,
            {
                "Library Announcement": {
                    "doctype": "Library Announcement2",
                    "field_map": {
                        "title": "title",
                        "message": "message",
                        "priority": "priority",
                        "date": "date",
                        "posted_by": "posted_by"
                    }
                }
            }
        )
        target_doc.insert()
        frappe.db.commit()   
        return target_doc

    def rename_announcement():
        old_name = "4vvla5e92v"  
        new_name = "Announcement-001"  
        frappe.rename_doc("Library Announcement", old_name, new_name)
        frappe.db.commit()
        frappe.msgprint(f"Renamed {old_name} to {new_name}")
        


    def delete_announcement(name):
        """Delete a specific Library Announcement document by name."""
        try:
            frappe.delete_doc("Library Announcement", name)
            frappe.db.commit()
            frappe.msgprint(f"Announcement '{name}' deleted successfully!")
            return f"Announcement '{name}' deleted successfully!"
        except Exception as e:
            frappe.db.rollback()
            frappe.msgprint(f"Error deleting announcement: {e}")
            return f"Error deleting announcement: {e}"

        

    # def show_system_settings():
    #     settings = frappe.get_system_settings("all")
    #     print(settings)
    def show_system_settings():
        """Fetch and return key system settings."""
        settings = {
            "Language": frappe.get_system_settings("language"),
            "Country": frappe.get_system_settings("country"),
            "Time Zone": frappe.get_system_settings("time_zone"),
            "Currency": frappe.get_system_settings("currency")
        }

        print("System Settings:")
        for key, value in settings.items():
            print(f"{key}: {value}")

        return settings


    def db_get_list_example(priority=None, limit=20):
        filters={}
        if priority:
            filters["priority"]=priority
            
        rows=frappe.db.get_list(
        "Library Announcement",
        fields=["name", "title", "priority", "date","posted_by"],
        filters=filters,
        limit=limit,
        )
        return rows


    def on_update(self):
        frappe.db.set_value(
            "Library Announcement",   
            self.name,               
            {
                "priority": "High",          
                "posted_by": "Updated User"  
            }
        )
        frappe.msgprint(f"Announcement '{self.name}' updated: Priority set to High, Posted By changed to Updated User.")
        frappe.db.commit()


        #exmaple for frappe.get_doc
        existing_doc=frappe.get_doc("Library Announcement","8a9pfrr1g7")
        frappe.msgprint(f"Existing Doc Title: {existing_doc.title}, Message: {existing_doc.message}")

        #example for frappe.get_last_doc()
        last_announcement=frappe.get_last_doc("Library Announcement")

        frappe.msgprint(
            msg=(
                f"Latest Announcment:\n\n"
                f"Title: {last_announcement.title}\n"
                f"Message: {last_announcement.message}\n"
                f"Date: {last_announcement.date}\n"
                f"Priority: {last_announcement.priority}\n"
                f"Posted By: {last_announcement.posted_by}"
            ),
            title="Most Recent Announcement",
            indicator="green"
        )




        #example for frappe.get_cached_doc
        cached_doc=frappe.get_cached_doc("Library Announcement","8a9pfrr1g7")
        
        frappe.msgprint(
            msg=(
                f"Cached Doc Announcement:\n\n"
                f"Title: {cached_doc.title}\n"
                f"Message: {cached_doc.message}\n"
                f"Date: {cached_doc.date}\n"
                f"Priority: {cached_doc.priority}\n"
                f"Posted By: {cached_doc.posted_by}"
            ),
            title="Cached Announcement",
            indicator="blue"
        )
        #exmaple for frappe.rename_doc
        # if self.title:
        #     new_name=frappe.scrub(self.title)

        #     if self.name!=new_name:
        #         try:
        #             frappe.rename_doc(
        #                 doctype="Library Announcement",
        #                 # old_name=self.name,
        #                 # new_name="8a9pfrr1g7",
        #                 merge=False,
        #                 forces=True
        #             )
        #             frappe.msgprint(f"Announcement renamed to: {new_name}")
        #         except frappe.DuplicateEntryError:
        #             frappe.msgprint(f"Announcement with name {new_name} already exists. Rename skipped.")


        #example for frappe.rendeer_template
        #load the html template file
        template_path=frappe.get_app_path(
            "library_management2",
            "templates",
            "includes",
            "announcment.html"
        )
        #reading the file content
        with open(template_path,"r",encoding="utf-8") as f:
            template=f.read()
        
        #prepare context(dat t ofill into temlate)
        context={
            "title":self.title,
            "message":self.message,
            "date":self.date or nowdate(),
            "priority":self.priority,
            "posted_by":self.posted_by
        }
        rendered_html=frappe.render_template(template,context)

        frappe.msgprint(rendered_html, title="Rendered Announcement Template")


        #example for frappe.utils methods
        today=nowdate()
        next_week=add_days(today,7)
        diff=date_diff(next_week,today)
        value="1234.56"
        safe_float=flt(value)
        safe_int=cint("10")

        rand_code=random_string(8)

        text="<b>Welcome to Library Management System!</b>"
        clean_text=strip_html_tags(text)

        frappe.msgprint(f"""
             Today: {today}<br>
             Next Week: {next_week}<br>
             Date Difference: {diff} days<br>
             Float: {safe_float}, Int: {safe_int}<br>
             Random Code: {rand_code}<br>
             Cleaned Text: {clean_text}
        """)
       # example for errror logs
        try:
                # Example risky code (division by zero)
                result = 10 / 0  # This will raise an exception

        except Exception as e:
            # Log error with custom title and message
            frappe.log_error(
                title="Error in Library Announcement Update",
                message=f"An unexpected error occurred: {str(e)}"
            )

            # Optional: show user-friendly message
            frappe.msgprint(" Something went wrong. Please contact the administrator.")


    def after_insert(self):
        if not getattr(self,"is_automated",False):
            new_doc=frappe.new_doc("Library Announcement")
            new_doc.title=f"Reminder:{self.title}"
            new_doc.message=f"This is an automated remainder for :{self.message}"
            new_doc.date=nowdate()
            new_doc.priority=self.priority
            new_doc.posted_by="Automated System"
            new_doc.is_automated=True
            new_doc.insert()
            frappe.db.commit()
            frappe.msgprint(f"Automated reminder announcement created with name: {new_doc.name}")

    
            