// URL where your Flask backend is running (from app.py)
const API_URL = "http://127.0.0.1:5000";

const educationSelect = document.getElementById("education");
const jobRoleSelect = document.getElementById("jobRole");
const citySelect = document.getElementById("city");
const form = document.getElementById("salaryForm");
const resultDiv = document.getElementById("result");
const resultAmount = document.getElementById("resultAmount");
const errorDiv = document.getElementById("error");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");

function fillSelect(selectEl, options) {
  selectEl.innerHTML = "";
  options.forEach((opt) => {
    const option = document.createElement("option");
    option.value = opt;
    option.textContent = opt;
    selectEl.appendChild(option);
  });
}

// Animate the salary number counting up
function animateNumber(el, target) {
  const duration = 600;
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const value = Math.floor(progress * target);
    el.textContent = `₹${value.toLocaleString("en-IN")}`;
    if (progress < 1) requestAnimationFrame(tick);
    else el.textContent = `₹${target.toLocaleString("en-IN")}`;
  }
  requestAnimationFrame(tick);
}

// Load dropdown values from the backend when the page opens
async function loadOptions() {
  try {
    const res = await fetch(`${API_URL}/options`);
    const data = await res.json();
    fillSelect(educationSelect, data.education_levels);
    fillSelect(jobRoleSelect, data.job_roles);
    fillSelect(citySelect, data.cities);
  } catch (err) {
    errorDiv.textContent = "Could not connect to backend. Make sure app.py is running on port 5000.";
    errorDiv.classList.remove("hidden");
  }
}

// Handle form submit -> call /predict
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");

  submitBtn.disabled = true;
  btnText.textContent = "Predicting...";

  const payload = {
    experience: document.getElementById("experience").value,
    education: educationSelect.value,
    job_role: jobRoleSelect.value,
    city: citySelect.value
  };

  try {
    const res = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (data.error) {
      errorDiv.textContent = data.error;
      errorDiv.classList.remove("hidden");
    } else {
      resultDiv.classList.remove("hidden");
      animateNumber(resultAmount, Math.round(data.predicted_salary));
    }
  } catch (err) {
    errorDiv.textContent = "Prediction failed. Check that the backend server is running.";
    errorDiv.classList.remove("hidden");
  } finally {
    submitBtn.disabled = false;
    btnText.textContent = "Predict Salary";
  }
});

loadOptions();