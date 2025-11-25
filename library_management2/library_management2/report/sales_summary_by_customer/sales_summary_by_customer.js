frappe.query_reports["Sales Summary by Customer"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label":__("From Date"),
			"fieldtype":"Date"
		},
		{
			"fieldname":"to_date",
			"label":__("To Date"),
			"fieldtype":"Date"
		},
		// {
		// 	"fieldname": "status",
		// 	"label": __("Status"),
		// 	"fieldtype": "Select",
		// 	"options": "\nDraft\nCompleted\nCancelled"
		// }
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Apply colors to specific columns
		if (column.fieldname === "total_sales" || column.fieldname === "avg_sale") {
			let color = "";
			let numValue = data[column.fieldname];
			
			if (numValue < 10000) {
				color = "blue";
			} else if (numValue >= 20000 && numValue <= 40000) {
				color = "green";
			} else {
				color = "red";
			}
			
			// Wrap in div with inline-block to maintain alignment
			value = `<div style="color:${color}; font-weight:bold; width:100%; display:inline-block;">${value}</div>`;
		}
		
		return value;
	}
};