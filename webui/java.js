
    
    
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




    const data = await response.json();

    currentVM = data.vm_name;  // <-- Store VM name
    console.log("VM started:", currentVM);


// End session function
async function endSession() {

    if (!currentVM) {
        alert("No active VM session.");
        return;
    }

    const confirmEnd = confirm("Are you sure you want to end this session?");
    if (!confirmEnd) return;

    try {
        const response = await fetch("/end-vm", {
        } else {
            output.textContent = `✅ You selected: ${select.options[select.selectedIndex].text}`;
            output.style.color = "green";
            const choice = `${select.options[select.selectedIndex].text}`;
            fetch("http://127.0.0.1:8000/request-vm", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                vm_name: currentVM
            })
        });

        if (!response.ok) {
            throw new Error("Failed to end session");
        }

        const result = await response.json();

        alert("Session ended successfully.");
        console.log(result);

        currentVM = null; // Clear stored VM

    } catch (error) {
        console.error("Error:", error);
        alert("Error ending session.");
    }
}


// Attach button listener
document.getElementById("endSessionBtn")
        .addEventListener("click", endSession);