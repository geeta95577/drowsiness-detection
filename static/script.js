// PAGE SWITCHING
function switchPage(page) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(page).classList.add("active");

    document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
    document.querySelector(`[data-page='${page}']`).classList.add("active");
}

document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
        switchPage(link.dataset.page);
    });
});

// CLOCK
setInterval(() => {
    const now = new Date();
    document.getElementById("current-time").innerText =
        now.toLocaleTimeString();
}, 1000);

// (Optional) Fake EAR update for frontend UI only
setInterval(() => {
    let fakeEAR = (Math.random() * 0.3 + 0.2).toFixed(2);
    document.getElementById("ear-value").innerText = fakeEAR;

    if (fakeEAR < 0.25) {
        document.getElementById("detection-status").classList.remove("safe");
        document.getElementById("detection-status").classList.add("drowsy");
        document.getElementById("detection-status").innerHTML =
            "<i class='fas fa-exclamation-triangle'></i> Drowsy";
    } else {
        document.getElementById("detection-status").classList.remove("drowsy");
        document.getElementById("detection-status").classList.add("safe");
        document.getElementById("detection-status").innerHTML =
            "<i class='fas fa-check-circle'></i> Safe";
    }
}, 1500);
