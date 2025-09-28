const API_BASE = "https://your-phishing-api.onrender.com"; // ⬅️ Replace after deployment

// ---------- SCAN URL ----------
document.getElementById("scanBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value.trim();
  const resultDiv = document.getElementById("result");

  if (!url) {
    resultDiv.innerText = "⚠️ Please enter a URL.";
    resultDiv.style.color = "#ffaa00";
    return;
  }

  resultDiv.innerText = "🔍 Scanning...";
  resultDiv.style.color = "#facc15";

  try {
    const response = await fetch(`${API_BASE}/api?url=${encodeURIComponent(url)}`);
    const data = await response.json();

    if (data.result === "Phishing") {
      resultDiv.innerText = "⚠️ PHISHING SITE DETECTED!";
      resultDiv.style.color = "#ff004c";
    } else if (data.result === "Safe") {
      resultDiv.innerText = "✅ SAFE SITE";
      resultDiv.style.color = "#00ff9c";
    } else {
      resultDiv.innerText = "❓ Unknown result";
      resultDiv.style.color = "#ffaa00";
    }
  } catch (error) {
    resultDiv.innerText = "❌ Backend not reachable";
    resultDiv.style.color = "#ff004c";
    console.error(error);
  }
});

// ---------- FETCH SCAN HISTORY ----------
async function loadHistory() {
  try {
    const res = await fetch(`${API_BASE}/history`);
    const logs = await res.json();
    const historyDiv = document.getElementById("history");
    historyDiv.innerHTML = "";

    logs.reverse().forEach((log) => {
      const date = new Date(log.timestamp).toLocaleString();
      historyDiv.innerHTML += `
        <div class="history-item">
          <span class="url">${log.url}</span>
          <span class="result ${log.result.toLowerCase()}">${log.result}</span>
          <span class="time">${date}</span>
        </div>
      `;
    });
  } catch (error) {
    console.error("Failed to load history:", error);
  }
}

// Load history if on history.html
if (document.getElementById("history")) {
  loadHistory();
}
