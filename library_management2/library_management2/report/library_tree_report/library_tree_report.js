frappe.query_reports["Library Tree Report"] = {
    onload: function(report) {
        report.page.set_title("Library Tree Report");
        report.page.add_inner_button('Expand All', () => {
        $('span.treegrid-expander-collapsed').click();  // expand all nodes
    });

    report.page.add_inner_button('Collapse All', () => {
        $('span.treegrid-expander-expanded').click();   // collapse all nodes
    });
    },
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (!data) return value;

        // Apply color based on the "type" field
        if (data.type === "Library") {
            value = `<span style="color: green; font-weight: 600;">${value}</span>`;
        } else if (data.type === "Section") {
            value = `<span style="color: blue;">${value}</span>`;
        } else if (data.type === "Shelf") {
            value = `<span style="color: orange;">${value}</span>`;
        } else if (data.type === "Book") {
            value = `<span style="color: red;">${value}</span>`;
        }

        return value;
    }
};
