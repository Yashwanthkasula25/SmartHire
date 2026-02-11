let currentProfile = null;

async function loadDashboard() {

    const token = localStorage.getItem("token");

    // ---------------- LOAD PROFILE ----------------
    const profileRes = await fetch(
        "http://127.0.0.1:8000/profile/me",
        {
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    );

    if (profileRes.ok) {
        const profile = await profileRes.json();
        currentProfile = profile;

        document.getElementById("profileName").innerText =
            profile.full_name || "Complete Profile";

        const emailElement = document.getElementById("profileEmail");
        if (emailElement) {
            emailElement.innerText = profile.email || "";
        }
    }

    // ---------------- LOAD APPLICATIONS ----------------
    const appRes = await fetch(
        "http://127.0.0.1:8000/applications/my",
        {
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    );

    const applications = await appRes.json();

    const container = document.getElementById("applicationsContainer");
    container.innerHTML = "";

    applications.forEach(app => {
        container.innerHTML += `
            <div class="application-card">
                <h4>${app.job.title}</h4>
                <p><b>Score:</b> ${app.resume_score}</p>
                <p><b>Status:</b> ${app.status}</p>
            </div>
        `;
    });
}

loadDashboard();


// ---------------- PROFILE MODAL ----------------

function openProfile() {
    document.getElementById("profileModal").style.display = "flex";

    if (currentProfile) {
        document.getElementById("updateFullName").value =
            currentProfile.full_name || "";

        document.getElementById("updateCompany").value =
            currentProfile.company_name || "";

        document.getElementById("updateExperience").value =
            currentProfile.experience_years || "";

        document.getElementById("updateSkills").value =
            currentProfile.skills || "";
    }
}

function closeProfile() {
    document.getElementById("profileModal").style.display = "none";
}
function showProfile() {
    document.getElementById("applicationsView").style.display = "none";
    document.getElementById("profileView").style.display = "block";

    if (currentProfile) {
        document.getElementById("viewFullName").innerText =
            currentProfile.full_name || "-";

        document.getElementById("viewCompany").innerText =
            currentProfile.company_name || "-";

        document.getElementById("viewExperience").innerText =
            currentProfile.experience_years || "-";

        document.getElementById("viewSkills").innerText =
            currentProfile.skills || "-";
    }
}

function showApplications() {
    document.getElementById("profileView").style.display = "none";
    document.getElementById("applicationsView").style.display = "block";
}


// ---------------- FORM SUBMIT ----------------

document.addEventListener("DOMContentLoaded", () => {

    const profileForm = document.getElementById("profileForm");

    if (!profileForm) return;

    profileForm.addEventListener("submit", async function(e) {

        e.preventDefault();

        const token = localStorage.getItem("token");

        const full_name =
            document.getElementById("updateFullName").value;

        const company_name =
            document.getElementById("updateCompany").value;

        const experience_years =
            document.getElementById("updateExperience").value;

        const skills =
            document.getElementById("updateSkills").value;

        const response = await fetch(
            "http://127.0.0.1:8000/profile/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({
                    full_name,
                    company_name,
                    experience_years,
                    skills
                })
            }
        );

        if (response.ok) {
            alert("Profile updated successfully");
            closeProfile();
            loadDashboard();
        } else {
            alert("Profile update failed");
        }
    });

});
