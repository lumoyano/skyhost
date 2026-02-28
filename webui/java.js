
    document.getElementById("getBtn").addEventListener("click", function () {
        const select = document.getElementById("mySelect");
        const output = document.getElementById("output");

        if (!select.value) {
            output.textContent = "⚠ Please select an option first.";
            output.style.color = "red";
        } else {
            output.textContent = `✅ You selected: ${select.options[select.selectedIndex].text}`;
            output.style.color = "green";
            const choice = `${select.options[select.selectedIndex].text}`;
            fetch("http://192.168.1.100:8000/request-vm", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ template: choice })
})
        }
    });
