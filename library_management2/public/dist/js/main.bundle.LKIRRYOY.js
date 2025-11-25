(() => {
  // ../library_management2/library_management2/public/main.bundle.js
  console.log("\u2705 Hello from MyApp Bundle!");
  console.log("\u2705 Custom Script Active!");
  fetch('/api/resource/Library Member?fields=["name","first_name","last_name"]&limit_page_length=5').then((response) => response.json()).then((data) => {
    console.log("Library Members:", data.data);
    const membersDiv = document.getElementById("members");
    membersDiv.innerHTML = data.data.map(
      (m) => `<p>${m.first_name} ${m.last_name}</p>`
    ).join("");
  }).catch((err) => console.error("Error fetching Library Members:", err));
})();
//# sourceMappingURL=main.bundle.LKIRRYOY.js.map
