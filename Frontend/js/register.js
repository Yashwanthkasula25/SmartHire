document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;
    const phone = document.getElementById("phone").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                role: role,
                phone: phone
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful!");
            window.location.href = "index.html";
        } else {
            alert(data.detail || "Registration failed");
        }

    } catch (error) {
        alert("Server error");
        console.error(error);
    }
});
