// Copyright (c) 2025, Gagan G R and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Transaction3", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Library Transaction3', {
    refresh: function(frm) {
        frappe.msgprint('Fetching table structure...');
         //if calling thorugh path ,ie method outside the class
        frm.call({
            method:"library_management2.library_management2.doctype.library_transaction3.library_transaction3.describe_transaction_table",
            callback: function(r) {
                console.log(r.message); // Shows list of fields in browser console
                frappe.msgprint('Description fetched! Check browser console (F12)');
            }
        });
        //if calling directly ,if method inside .py class
    //     frm.call("describe_transaction_table")
    // .then(r => {
    //     console.log(r.message);  // response from Python method
    //     frappe.msgprint("Description fetched! Check console.");
    // });
    }
});

