document.getElementById("scanBtn")?.addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value;
  const resultDiv = document.getElementById("result");

  resultDiv.innerText = "🔍 Scanning...";
  resultDiv.style.color = "#facc15";

  try {
    const res = await fetch(`http://127.0.0.1:8000/api?url=${encodeURIComponent(url)}`);
    const data = await res.json();

    if (data.result === "Phishing") {
      resultDiv.innerText = "⚠️ PHISHING SITE DETECTED!";
      resultDiv.style.color = "#ff004c";
    } else {
      resultDiv.innerText = "✅ SAFE SITE";
      resultDiv.style.color = "#00ff9c";
    }
  } catch (err) {
    resultDiv.innerText = "❌ Error connecting to backend";
    resultDiv.style.color = "#ff004c";
  }
});
