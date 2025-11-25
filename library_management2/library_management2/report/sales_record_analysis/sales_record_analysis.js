frappe.query_reports["Sales Record Analysis"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_end()
        },
        {
            "fieldname": "customer_name",
            "label": __("Customer"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": ["Draft", "Completed", "Cancelled"]
        }
    ],
    onload: function(report) {
    frappe.query_report.filters.forEach(filter => {
        filter.df.onchange = () => {
            let from_date = frappe.query_report.get_filter_value("from_date");
            let to_date = frappe.query_report.get_filter_value("to_date");

            if (from_date && to_date && from_date > to_date) {
                frappe.msgprint({
                    title: __("Invalid Date Range"),
                    message: __("From Date cannot be greater than To Date."),
                    indicator: "red"
                });

                frappe.query_report.set_filter_value("to_date", "");
            }
        };
    });
}
};
