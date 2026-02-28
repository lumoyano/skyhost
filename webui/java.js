
    
    
document.getElementById("getBtn").addEventListener("click", function () {
    const select = document.getElementById("mySelect");
    const output = document.getElementById("output");

    if (!select.value) {
            output.textContent = "⚠ Please select an option first.";
            output.style.color = "red";
    } 
    else {
        output.textContent = `Starting VM Client`;
        output.style.color = "white";
        output.style.fontFamily = "Trebuchet MS"
        const choice = `${select.options[select.selectedIndex].text}`;
        fetch("http://192.168.56.101:8000/request-vm", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ template: choice })})
    } })
document.getElementById('getBtn').addEventListener('click', function () {
this.disabled = true; // Disable the button
console.log('Button disabled');
});


let currentVM = null;  // This should be set when VM is created

async function endSession() {

    if (!currentVM) {
        alert("No active VM session.");
        return;
    }

    const confirmEnd = confirm("Are you sure you want to end this session?");
    if (!confirmEnd) return;

    try {
        const response = await fetch("/end-vm", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                vm_name: currentVM
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to end VM");
        }

        alert("Session ended.");
        currentVM = null;

    } catch (err) {
        console.error(err);
        alert("Error ending session.");
    }
}

document.getElementById("endSessionBtn")
        .addEventListener("click", endSession);