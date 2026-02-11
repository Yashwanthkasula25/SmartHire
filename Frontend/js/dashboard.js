async function loadApplications() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/applications/my",
        {
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    );

    const applications = await response.json();

    const container = document.getElementById("applicationsContainer");
    container.innerHTML = "";

    applications.forEach(app => {

        const div = document.createElement("div");
        div.className = "application-card";

        div.innerHTML = `
            <h3>${app.job_title}</h3>
            <p><b>Score:</b> ${app.score}</p>
            <p><b>Status:</b> ${app.status}</p>
        `;

        container.appendChild(div);
    });
}

loadApplications();
