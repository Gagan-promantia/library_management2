import frappe
from frappe.model.document import Document

class Student(Document):
   pass



































@frappe.whitelist()
def check_student_info(student_name, student_email):
    if student_email and "@" in student_email:
        return f"Student {student_name} has a valid email: {student_email}"
    else:
        return f"Invalid email for student {student_name}"

@frappe.whitelist()
def get_student_details(email):
    try:
        # Fetch the student by email
        student = frappe.db.get_doc("Student", {"email": email})

        # Fetch related course (linked via course field)
        course_data = {}
        if student.course:
            course_doc = frappe.db.get_doc("Course Enrollment", student.course)
            course_data = {
                "course_name": course_doc.course_name,
                "instructor": course_doc.instructor,
                "duration": course_doc.duration,
                "fees": course_doc.fees,
                "start_date": course_doc.start_date
            }

        # Return combined data
        return {
            "student_name": student.student_name,
            "age": student.age,
            "email": student.email,
            "status": student.status,
            "total_marks": student.total_marks,
            "course": course_data
        }

    except frappe.DoesNotExistError:
        return {"error": "Student not found"}