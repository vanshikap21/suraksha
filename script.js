function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
}

function showReminder(type) {
  alert(`Reminder set for ${type} tablet at 10:00 AM daily!`);
}

document.getElementById('symptom-form')?.addEventListener('submit', function (e) {
  e.preventDefault();
  const dangerSigns = Array.from(document.querySelectorAll('#symptom-form input:checked'))
    .map(input => input.value);
  if (dangerSigns.length > 0) {
    alert("⚠️ You selected danger signs! Please visit your nearest PHC or contact your ASHA worker.");
  } else {
    alert("✅ No critical symptoms reported.");
  }
});

function generatePDF() {
  alert("📄 PDF report generated (demo only). Add backend for real PDF.");
}

function speak(text) {
  const msg = new SpeechSynthesisUtterance(text);
  msg.lang = 'hi-IN'; // For Hindi, use 'en-US' for English
  speechSynthesis.speak(msg);
}

async function uploadImage() {
  const input = document.getElementById('imageInput');
  if (!input.files[0]) return alert("Please select an image.");
  
  const formData = new FormData();
  formData.append("image", input.files[0]);

  const res = await fetch("/predict-image", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("result").innerText =
    `Result: ${data.result.label.toUpperCase()} (${data.result.confidence}% confidence)\nHemoglobin: ${data.result.hemoglobin}`;
  document.getElementById("last-result").innerText = data.result.label;
}
