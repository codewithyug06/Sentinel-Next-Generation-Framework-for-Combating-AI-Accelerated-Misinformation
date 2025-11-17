// popup.js — Refocused for Cognitive Shield

function renderSentinel(result) {
    const statusContainer = document.getElementById('status-container');
    const statusIcon = document.getElementById('status-icon');
    const statusText = document.getElementById('status-text');
    const alertsContainer = document.getElementById('alerts-container');
    const initialMessage = document.getElementById('initial-message');

    // Clear previous state
    alertsContainer.innerHTML = '';
    initialMessage.classList.add('hidden');

    if (!result || !result.status) {
        initialMessage.classList.remove('hidden');
        statusText.textContent = 'No analysis yet';
        statusContainer.className = 'mb-3 p-3 rounded-lg flex items-center bg-slate-100';
        statusIcon.className = 'w-5 h-5 rounded-full mr-3 bg-slate-400';
        return;
    }

    const status = result.status.toLowerCase();
    
    // Update main status bar
    statusText.textContent = `Analysis: ${status.charAt(0).toUpperCase() + status.slice(1)}`;
    let colorClasses = 'bg-slate-100';
    let iconColor = 'bg-slate-400';

    if (status === 'green') {
        colorClasses = 'bg-green-100 text-green-800';
        iconColor = 'bg-green-500';
        statusText.textContent = 'No manipulative techniques detected';
    } else if (status === 'yellow') {
        colorClasses = 'bg-yellow-100 text-yellow-800';
        iconColor = 'bg-yellow-500';
    } else if (status === 'red') {
        colorClasses = 'bg-red-100 text-red-800';
        iconColor = 'bg-red-500';
    }
    statusContainer.className = `mb-3 p-3 rounded-lg flex items-center ${colorClasses}`;
    statusIcon.className = `w-5 h-5 rounded-full mr-3 ${iconColor}`;

    // Display detailed alerts
    if (result.alerts && result.alerts.length > 0) {
        result.alerts.forEach(alert => {
            const alertElement = document.createElement('div');
            alertElement.className = 'bg-white border border-slate-200 p-3 rounded-lg mb-2 shadow-sm';
            
            const titleElement = document.createElement('h3');
            titleElement.className = 'font-semibold text-sm mb-1';
            titleElement.textContent = alert.title;
            
            const contentElement = document.createElement('p');
            contentElement.className = 'text-sm text-slate-600';
            contentElement.textContent = alert.content;
            
            alertElement.appendChild(titleElement);
            alertElement.appendChild(contentElement);
            alertsContainer.appendChild(alertElement);
        });
    } else if (status === 'green') {
        const noIssuesElement = document.createElement('div');
        noIssuesElement.className = 'text-center text-slate-500 mt-4 text-sm';
        noIssuesElement.innerHTML = `<p class="font-semibold">All clear!</p><p>This content appears to be straightforward.</p>`;
        alertsContainer.appendChild(noIssuesElement);
    }
}


async function loadAndRender() {
    try {
        const { sentinel_result } = await chrome.storage.local.get("sentinel_result");
        renderSentinel(sentinel_result);
    } catch (e) {
        console.error("Popup load error", e);
        document.getElementById("alerts-container").innerText = "Error loading analysis.";
    }
}

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
    loadAndRender();

    // Live updates: re-render when background updates storage
    chrome.storage.onChanged.addListener((changes, area) => {
        if (area === "local" && changes.sentinel_result) {
            renderSentinel(changes.sentinel_result.newValue);
        }
    });
});
