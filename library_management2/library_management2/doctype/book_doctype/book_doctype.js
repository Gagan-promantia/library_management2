// // frappe.ui.form.on('Book Doctype', {
// //     book_title(frm) {
// //         if (!frm.doc.book_title) return;

// //         frappe.call({
// //             method: "library_management2.library_management2.doctype.book_doctype.book_doctype.get_book_info",
// //             args: {
// //                 book_title: frm.doc.book_title
// //             },
// //             callback: function(r) {
// //                 if (!r.message) return;

// //                 if (r.message.error) {
// //                     frappe.msgprint(r.message.error);
// //                 } else {
// //                     frm.set_value("author", r.message.author);
// //                     frm.set_value("isbn", r.message.isbn);

// //                     frappe.msgprint("Fetched Author & ISBN using AJAX");
// //                 }
// //             }
// //         });
// //     }
// // });

// frappe.ui.form.on('Book Doctype', {
//     book_title(frm) {
//         if (!frm.doc.book_title) return;

//         frappe.call({
//             method: "library_management2.library_management2.doctype.book_doctype.book_doctype.get_book_info",
//             args: {
//                 book_title: frm.doc.book_title
//             },
//             freeze: true,
//             async: true,

//             callback: function (r) {
//                 if (!r.message) return;

//                 if (r.message.error) {
//                     frappe.msgprint(r.message.error);
//                     return;
//                 } else {
//                     frm.set_value("author", r.message.author);
//                     frm.set_value("isbn", r.message.isbn);
//                     frm.set_value("shelf", r.message.shelf);
//                     frm.set_value("publisher", r.message.publisher);
//                     frm.set_value("publication_year", r.message.publication_year);
//                     frm.set_value("description", r.message.description);
//                 }
//             },

//             error: function (r) {
//                 frappe.msgprint("Server error occurred");
//             },

//             always: function (r) {
//                 console.log("AJAX call completed");
//             }
//         });
//     }
// });
