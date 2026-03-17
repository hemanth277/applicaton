async function search(){
    const query = document.getElementById("query").value;
    const container = document.getElementById("results");

    container.innerHTML = "<p>Searching...</p>";

    try {
        const res = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        if (!res.ok) {
            const text = await res.text();
            container.innerHTML = `<p style=\"color:red\">Error: ${res.status} ${res.statusText} - ${text}</p>`;
            return;
        }

        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = "<p>No results found.</p>";
            return;
        }

        container.innerHTML = "";

        const table = document.createElement("table");
        table.className = "results-table";

        const thead = document.createElement("thead");
        thead.innerHTML = `
<tr>
<th>#</th>
<th>Name</th>
<th>Description</th>
<th>Open</th>
</tr>
`;
        table.appendChild(thead);

        const tbody = document.createElement("tbody");

        data.forEach((item, index) => {
            const row = document.createElement("tr");
            const href = item.link || "";
            const normalizedLink = href.startsWith("//") ? `https:${href}` : href;

            row.innerHTML = `
<td>${index + 1}</td>
<td>${item.title || "No title"}</td>
<td>${item.description || "No description available."}</td>
<td><a href="${normalizedLink}" target="_blank" rel="noopener">Open</a></td>
`;

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        container.appendChild(table);
    } catch (err) {
        container.innerHTML = `<p style=\"color:red\">Error: ${err.message}</p>`;
    }
}