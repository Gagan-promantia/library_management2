// Copyright (c) 2025, Gagan G R and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Members", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Library Members",{
    refresh(frm){
        if(!frm.is_new()){
            frm.add_custom_button(("show Email"),()=>{
                if(frm.doc.email){
                frappe.msgprint(`Member Email:${frm.doc.email}`);
                }else{
                    frappe.msgprint(`NO email found for this member`);
                }
            });
        }
    }
});

frappe.ui.form.on('Library Members', {
    first_name:function(frm){
        //when first name changes this wil update the ful name
        frm.set_value('full_name',frm.doc.first_name+ ' '+(frm.doc.last_name || ''));
    },
    last_name:function(frm){
        //when last name changes this wil update the ful name
        frm.set_value('full_name',frm.doc.first_name+ ' '+(frm.doc.last_name || ''));
    }
}
);

frappe.ui.form.on("Library Members", {
    refresh(frm){
        frm.add_custom_button("Update Email",function(){
            frm.set_value("email","updatedemail@example.com");
            frm.save();
        });
    }
});

frappe.ui.form.on("Library Members",{
    email(frm){
        //disabling if the email is not entered
        if(!frm.doc.email){
            frm.disable_save();
            frappe.msgprint("Please enter email to enable save");
        }else{
            frm.enable_save();
        }
    }
});

frappe.ui.form.on("Library Members",{
    refresh(frm){
        if(!frm.is_new()){
        frm.add_custom_button("Send Email",function(){
            frm.email_doc();
        },"Actions");
        frm.add_custom_button("Reload Data",function(){
            frm.reload_doc();
        },"Actions");
        frm.change_custom_button_type("Send Email","Actions","primary");
        frm.change_custom_button_type("Reload Data","Actions","danger");
    }
    }
});


frappe.ui.form.on("Library Members",{
    refresh(frm){
        frm.add_custom_button("Reload",function(){
            frm.reload_doc();
            frappe.msgprint("Document Reloaded Successfully");
        })
    }
});

frappe.ui.form.on("Library Members",{
    refresh(frm){
        frm.add_custom_button("Update City",function(){
            frm.set_value("city","New City");
            frm.refresh();
            frappe.msgprint("City updated to New City");
        })
    }
});

frappe.ui.form.on("Library Members",{
    refresh(frm){
        frm.add_custom_button("Check save ",function(){
          if (frm.is_dirty()){
            frappe.msgprint("There are changes that need to be save");
          }else{
            frappe.msgprint("There are no changes to save");
          }
        });
    }
});

frappe.ui.form.on("Library Members",{
    refresh(frm){
        if(frm.is_new()){
            frm.set_intro("Please  fill al l member details before saving","blue");
        }else if(!frm.doc.email){
            frm.set_intro("Email is missing please update it ","yellow");
        }else{
            frm.set_intro("all members details looke complete","green");
        }
    }
});


frappe.ui.form.on("Library Members",{
    refresh(frm){
        if(!frm.is_new()){
            frm.remove_custom_button("Send Email");

            frm.add_custom_button("Send Email",function(){
                frappe.msgprint("Custom email button clickedd");
            },"Actions");

            frm.change_custom_button_type("Send Email","Actions","primary");
        }
        frm.toggle_reqd('first_name',true);
        frm.toggle_display('city',frm.doc.age===25);
    }
});


frappe.ui.form.on("Library Members",{
    age(frm){
    if(frm.doc.age===20){
        frm.set_df_property("age","reqd",true);
    }else{
        frm.set_df_property("age","reqd",false);
    }
}
});

//child table script



frappe.ui.form.on("Library Members", {
    //example for setup()
    setup(frm) {
        frm.set_query("membership_type", "membership_details", function() {
            return {
                filters: {
                    is_active: 1
                }
            };
        });

        console.log("Setup event triggered for Library Members");
    },
    

    //example for before_load
    before_load(frm){
        console.log("Before load triggered for Library Members");
        if(!frm.doc.full_name && frm.doc.first_name && frm.doc.last_name){
            frm.set_value("full_name",frm.doc.first_name +" "+frm.doc.last_name);
        }
    },
    //example for onload
    onload(frm){
        console.log("onload event triggered for library memberes");
        if(!frm.doc.age){
            frm.set_value("age",18);
        }
    },

    //example for onload_post_render(frm)
    onload_post_render(frm){
        console.log("onload_post_render event triggered for libraray memeber");

        if(!frm.doc.first_name){
            frm.fields_dict.first_name.$input.focus();
        }

        $(frm.fields_dict.full_name.wrapper)
            .css("background-color","#fff3cd")
            .css("border","1px solid #ffeeba");
    },
    //example for validate
    validate(frm) {
        console.log("Validate event triggered for Library Members");
        
        if (frm.doc.age < 18) {
            frappe.throw("Member must be at least 18 years old");
        }
    },
    before_save(frm) {
        console.log("Before Save event triggered for Library Members");
        if (frm.doc.age >= 60 && frm.doc.full_name) {
            // Avoid repeating "Senior" if already added
            if (!frm.doc.full_name.toLowerCase().startsWith("senior")) {
                frm.set_value("full_name", "Senior " + frm.doc.full_name);
            }
        }
    },
    after_save(frm){
        console.log("After Save event triggered for LIbrary Members");

        frappe.msgprint(`Member ${frm.doc.full_name} has been saved successfully!`);
    },
    before_submit(frm){
        console.log("After submt is executed for library members");

        if(!frm.doc.membership_details){
            frappe.throw("Please select the membership type before submitting");
        }
    },
    on_submit(frm) {
        console.log("on_submit event triggered for Library Members");
        frappe.msgprint("Form submitted successfully!");
    },
    before_cancel(frm){
        console.log("Before cancel triggered for library members");
        if(frm.doc.age>50){
            frappe.throw("Cannot cancel this member age is above 50")
        }
    },
    after_cancel(frm){
        console.log("After cancel triggered for library members");

        frm.set_value("status","cancelled");
        frm.refresh_field("status");
    },
    before_discard(frm) {
        console.log("Before discard triggered for Library Members");
        frappe.msgprint("You are about to discard unsaved changes!");
    },
    after_discard(frm) {
        frappe.msgprint(" after_discard triggered: Changes have been discarded.");
        console.log("after_discard event executed for Library Members");
    },
    timeline_refresh(frm){
        console.log("Time line refreshed for library members");
        frappe.msgprint("The timeline has been refreshed!");
        if(frm.timeline.wrapper){
            frm.timeline.wrapper.css("background-color","#cccaf0ff");
        }
        frm.trigger("show_message");
        console.log("frm.triiger function executed")
    },
    show_message: function(frm) {
        frappe.msgprint("Form is refreshed");
    },
   membership_details_on_form_rendered(frm, grid_row) {
        console.log("Child row form opened for Membership Details");
        //frappe.msgprint("Child table form opened successfully!");
         // Wait for a short moment to ensure the grid form is ready
        setTimeout(() => {
            // Safely check if grid_form exists
            if (!grid_row.grid_form || !grid_row.grid_form.fields_dict) {
                console.warn("Grid form not yet ready");
                return;
            }

            // Get the row document
            let row = grid_row.doc;
            console.log("Row data:", row);
        
        if (grid_row.grid_form.fields_dict["start_date"]) {
            $(grid_row.grid_form.fields_dict["start_date"].$wrapper)
                .css("background-color", "#e3f2fd")  // light blue background
                .css("border", "1px solid #2196f3");
            console.log("Highlighted start_date field");
        }
    },300)
    },
    age(frm){
        if(frm.doc.age<18){
            frappe.msgprint("Member must be 18 or older!");
        }
    },
    get_email_recipient_filters(frm, field) {
        return {
            filters: {
                is_active: 1,
                membership_type: frm.doc.membership_type
            }
        };
    },
     after_save:function(frm){
        if(frm.doc.age===35){
            frm.toggle_enable('age',false);
        }
    },
    after_save: function(frm) {
        console.log("add child executed");
        let row = frm.add_child("membership_details");
        row.start_date = frappe.datetime.nowdate();
        frm.refresh_field("membership_details");
    },

   refresh: function(frm) {
        frm.add_custom_button("Check Age", function() {
            frm.call({
                method:library_management2.library_management2.library_management2.doctype.library_members.library_members.check_age,//"check_age",  
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(r.message);
                    }
                }
            });
        });
        frm.add_custom_button("Show selected rows",function(){
             let grid = frm.fields_dict.membership_details.grid;
             let selected = grid.get_selected_children();

            //check if user selected any rows
           if (selected && selected.length > 0) {
                let row_names = selected.map(row => row.name);
                frappe.msgprint("You selected rows: " + row_names.join(", "));
                console.log("Selected rows:", selected);
            } else {
                frappe.msgprint(" No rows selected!");
            }
        });
        frm.add_custom_button("Add Membership via Dialog",function(){
            let d =new frappe.ui.Dialog({
                title:"Enter Membership Details",
                fields:[
                   {
                        label: "First Name",
                        fieldname: "first_name",
                        fieldtype: "Data",
                        reqd: 1
                    },
                    {
                        label: "Last Name",
                        fieldname: "last_name",
                        fieldtype: "Data",
                        reqd: 1
                    },
                    {
                        label: "Age",
                        fieldname: "age",
                        fieldtype: "Int"
                    },
                    {
                        label: "City",
                        fieldname: "city",
                        fieldtype: "Data"
                    }
                ],
                primary_action_label:"Save Member",
                primary_action(values){
                    frm.set_value("first_name",values.first_name);
                    frm.set_value("last_name", values.last_name);
                    frm.set_value("age", values.age);
                    frm.set_value("city", values.city);

                    frappe.msgprint("Member Details Added Successfully!");
                    d.hide();
                }

            });
            d.show();
        });
    },
    after_save: function(frm) {
        console.log("frappe msgprint executing");
        frappe.msgprint({
            title: __('Notification'),
            indicator: 'green',
            message: __('Library Membe r saved successfully!'),
            primary_action: {
                label: 'View Details',
                action() {
                    frappe.msgprint({
                        title: __('Member Info'),
                        message: __(
                            'Name: {0} {1}<br>Age: {2}<br>City: {3}',
                            [frm.doc.first_name, frm.doc.last_name, frm.doc.age, frm.doc.city]
                        )
                    });
                }
            }
        });
    },
    refresh: function(frm) {
        frm.add_custom_button("Enter Details", function() {

            frappe.prompt([
                {
                    label: 'City',
                    fieldname: 'city',
                    fieldtype: 'Data'
                },
                {
                    label: 'Age',
                    fieldname: 'age',
                    fieldtype: 'Int'
                }
            ],
            function(values) {
                //  Validation logic before accepting
                if (values.age < 18) {
                    frappe.msgprint({
                        title: __('Validation Error'),
                        message: __('Age must be at least 18 to register.'),
                        indicator: 'red'
                    });
                    // stop the process
                    frappe.throw(__('Cannot proceed. Please enter a valid age.'));
                }

                //  If valid, update form fields
                frm.set_value('city', values.city);
                frm.set_value('age', values.age);

                frappe.msgprint({
                    title: __('Success'),
                    message: __('Details saved successfully!'),
                    indicator: 'blue'
                });
            },
            'Enter Member Details',   // Dialog title
            'Save Details'            // Button label
            );

        });
        frm.add_custom_button("Clear City", function() {

            frappe.confirm(
                'Are you sure you want to clear the City field?',
                function() {
                    //  Yes clicked
                    frm.set_value('city', '');
                    frappe.msgprint(__('City has been cleared.'));
                },
                function() {
                    //  No clicked
                    frappe.msgprint(__('Action cancelled.'));
                }
            );

        });
        frm.add_custom_button("Delete Member", function() {

            frappe.warn(
                'Delete Confirmation', // title
                'You are about to delete this member. This action cannot be undone.', // message

                //  proceed_callback
                function() {
                    // Call Frappe's delete API
                    frappe.call({
                        method: "frappe.client.delete",
                        args: {
                            doctype: frm.doctype,
                            name: frm.doc.name
                        },
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.msgprint(__('Record deleted successfully.'));
                                frappe.set_route('List', frm.doctype); // go back to list view
                            }
                        }
                    });
                    frappe.msgprint(__('Record deleted successfully.'));
                },

                //  cancel_callback
                function() {
                    frappe.msgprint(__('Deletion cancelled.'));
                },

                //  options (optional)
                {
                    indicator: 'red',  // color of title indicator
                    primary_action_label: 'Delete' // text for confirm button
                }
            );

        });
    },
    after_save: function(frm) {
        frappe.show_alert({
            message: __('Member saved successfully!'),
            indicator: 'green'
        }, 4);
    }
    });
    frappe.ui.form.on("Library Members", {
        before_cancel: function(frm) {
            // Skip cancelling related doctypes automatically
            frm.ignore_doctypes_on_cancel_all(["Library Transaction", "Book Issue"]);
            frappe.msgprint("Book Issue and Library Transaction will not be cancelled automatically.");
        },
        refresh: function(frm) {
        frm.add_custom_button('Start Process', function() {
            let total = 5;
            for (let i = 1; i <= total; i++) {
                setTimeout(() => {
                    frappe.show_progress(
                        'Processing Members',
                        i,
                        total,
                        `Processing record ${i} of ${total}`,
                        true
                    );
                }, i * 1000);
            }
        });
         frm.add_custom_button('Add New Member', function() {
            // Create and open a new document of type "Library Members"
            frappe.new_doc('Library Members', {
                first_name: 'Gagan',
                last_name: 'Kumar',
                age: 25,
                city: 'Bangalore'
            });
        });
        frm.add_custom_button('Select Books', function() {

            new frappe.ui.form.MultiSelectDialog({
                doctype: "Book",
                target: frm,
                setters: {
                    status: 'Available'
                },
                get_query() {
                    return {
                        filters: {
                            status: 'Available'
                        }
                    };
                },
                action(selections) {
                    frappe.msgprint(`Books selected: ${selections.join(", ")}`);

                    // Optionally, add each book to a child table
                    selections.forEach(book => {
                        let row = frm.add_child('membership_details');
                        row.book = book;
                    });
                    frm.refresh_field('membership_details');
                }
            });

        });

    },
    

    // refresh: function(frm) {

    //     let row=frappe.get_doc(cdt,cdn);
    //     if(row.start_date){
    //         let end_date=frappe.datetime.add_days(row.start_date,365);
    //         frappe.model.set_value(cdt,cdn,"end_date",end_date);

    //     }
    // },
    membership_details_add(frm, cdt, cdn) {
        // Get the row just added
        let row = frappe.get_doc(cdt, cdn);
        // Example: Show a message
        frappe.msgprint(`A new membership row was added for ${frm.doc.full_name} `);

        // Example: Initialize start_date to today if empty
        if(!row.start_date) {
            frappe.model.set_value(cdt, cdn, "start_date", frappe.datetime.get_today());
        }
    },
    before_membership_details_remove(frm, cdt, cdn) {
        let row=frappe.get_doc(cdt,cdn);
        frappe.confirm('Are you sure want to delete the membership ')
    },

    membership_details_remove(frm,cdt,cdn){
        frappe.msgprint("A membership row has been deleted");
    },
     membership_details_move(frm, cdt, cdn) {
        // Row has been moved, fetch all rows
        let rows = frm.doc.membership_details;

        // Example: Recalculate a sequence field
        rows.forEach((row, index) => {
            frappe.model.set_value(row.doctype, row.name, "sequence", index + 1);
        });
    },
    form_render(frm, cdt, cdn) {
        // Get the row being rendered
        let row = frappe.get_doc(cdt, cdn);

        console.log("Child row form opened:", row);
        frappe.show_alert(`Editing membership starting on ${row.start_date || "N/A"}`);
    },   

});


