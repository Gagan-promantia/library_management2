// Copyright (c) 2025, Gagan G R and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Memeber3", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Library Memeber3",{
    refresh(frm){
        if(!frm.is_new()){
            frm.add_custom_button(_("show Email"),()=>{
                if(frm.doc.email){
                frappe.msgprint('Member Email:${frm.doc.email}');
                }else{
                    frappe.msgprint('NO email found for this member');
                }
            });
        }
    }
});