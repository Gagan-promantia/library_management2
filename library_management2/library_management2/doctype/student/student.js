// Copyright (c) 2025, Gagan G R and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Student', {
    refresh(frm) {
        frm.add_custom_button('Check Student Info', function() {
            frappe.call({
                method: "library_management2.library_management2.doctype.student.student.check_student_info",
                args: {
                    student_name: frm.doc.student_name,
                    student_email: frm.doc.email_id
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint("Server Response: " + r.message);
                    }
                },
                error: function(r) {
                    console.log("Error:", r);
                }
            })
        })
    },
    onload: function(frm) {
        if(frm.doc.email){  // make sure email is present
            frappe.call({
                method: "library_management2.library_management2.doctype.student.student.get_student_details",
                args: {
                    email: frm.doc.email
                },
                callback: function(r) {
                    if(r.message && !r.message.error){
                        console.log("Student Name:", r.message.student_name);
                        console.log("Course Name:", r.message.course.course_name);
			//  to set the value of student ,course total marks 
                        // Optional: set fields on the form
                        frm.set_value('total_marks', r.message.total_marks);
                        frm.refresh_field('total_marks');
                    } else {
                        frappe.msgprint(r.message.error || "No data found");
                    }
                }
            });
        }
    }
});
