console.log("📚 Library Books Script Active!");

// Fetch available books from the Library Book doctype
frappe.call({
    method: 'frappe.client.get_list',
    args: {
        doctype: 'Library Book',
        fields: ['name', 'title', 'author', 'status'],
        filters: {
            status: 'Available'
        },
        limit_page_length: 10
    },
    callback: function(response) {
        console.log("Available Books:", response.message);

        const booksDiv = document.getElementById("books");
        if (booksDiv) {
            if (response.message.length > 0) {
                booksDiv.innerHTML = response.message.map(
                    b => `
                    <div class="book-item" style="margin-bottom:10px;">
                        <strong>${b.title}</strong><br>
                        <span>Author: ${b.author}</span><br>
                        <span>Status: ${b.status}</span>
                    </div>`
                ).join("");
            } else {
                booksDiv.innerHTML = "<p>No books available right now.</p>";
            }
        }
    }
});
