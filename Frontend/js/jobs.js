async function loadJobs() {


const token = localStorage.getItem("token");

const response = await fetch("http://127.0.0.1:8000/jobs", {
    headers: {
        "Authorization": "Bearer " + token
    }
});

const jobs = await response.json();

const container = document.getElementById("jobsContainer");
container.innerHTML = "";

jobs.forEach(job => {
    const div = document.createElement("div");
    div.className = "job-card";

    div.innerHTML = `
        <h3>${job.title}</h3>
        <p>${job.description}</p>
        <button onclick="applyJob(${job.id})">Apply</button>
    `;

    container.appendChild(div);
});


}

loadJobs();
