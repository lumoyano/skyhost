
    
    
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