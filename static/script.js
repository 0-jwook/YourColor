document.getElementById("colorForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const colorInput = document.getElementById("colorInput").value;

    const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hex_color: colorInput }),
    });

    if (response.ok) {
        const data = await response.json();
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = `<h2>Recommended Colors for ${data.input_color}</h2>`;
        data.recommended_colors.forEach((color) => {
            const colorBox = document.createElement("div");
            colorBox.style.backgroundColor = color;
            colorBox.textContent = color;
            colorBox.className = "color-box";
            resultsDiv.appendChild(colorBox);
        });
    } else {
        alert("Failed to fetch recommended colors!");
    }
});
