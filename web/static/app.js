// CHRONOREVIVE // HAUTE HORLOGERIE KINEMATICS & ATELIER ENGINE

let audioCtx = null;
let soundEnabled = true;
let currentVph = 18000;
let balanceAngle = 0;
let lastTickSide = 0;
let animId = null;

document.addEventListener("DOMContentLoaded", () => {
  initEscapementAnimation();
  setupAudioToggle();
  setupVphSelector();
  setupMacroSlider();
  setupOrderTracking();
  setupAppraisalForm();

  // Load default order
  trackOrder("CR-8492");
});

// 1. Escapement Canvas Simulation
function initEscapementAnimation() {
  const canvas = document.getElementById("escapement-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let startTime = performance.now();

  function animate(now) {
    const elapsedSec = (now - startTime) / 1000;
    const freqHz = (currentVph / 3600) / 2; // e.g. 18000 vph = 2.5 Hz oscillation
    const omega = 2 * Math.PI * freqHz;
    const ampRad = 0.55; // ~31° balance oscillation amplitude

    balanceAngle = ampRad * Math.sin(omega * elapsedSec);

    // Pallet fork deflection angle (-0.12 to +0.12 rad)
    const forkAngle = Math.sign(balanceAngle) * 0.12;

    // Detect zero crossings to trigger mechanical tick
    const currentSide = Math.sign(Math.cos(omega * elapsedSec));
    if (currentSide !== lastTickSide && soundEnabled) {
      lastTickSide = currentSide;
      playMechanicalTick(currentSide > 0 ? 3200 : 2800);
    }

    renderEscapementScene(ctx, canvas.width, canvas.height, balanceAngle, forkAngle, elapsedSec);
    animId = requestAnimationFrame(animate);
  }

  animId = requestAnimationFrame(animate);
}

function renderEscapementScene(ctx, w, h, bAngle, fAngle, time) {
  ctx.fillStyle = "#060911";
  ctx.fillRect(0, 0, w, h);

  // Background grid / caliper concentric circles
  ctx.strokeStyle = "rgba(212, 175, 55, 0.08)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(w / 2, h / 2, 140, 0, Math.PI * 2);
  ctx.arc(w / 2, h / 2, 100, 0, Math.PI * 2);
  ctx.arc(w / 2, h / 2, 60, 0, Math.PI * 2);
  ctx.stroke();

  // Left side: Escape Wheel (Center at X: 280, Y: 170)
  const escX = 300;
  const escY = 170;
  const escRadius = 75;
  const escRotation = (time * (currentVph / 3600) * 0.1) % (Math.PI * 2);

  ctx.save();
  ctx.translate(escX, escY);
  ctx.rotate(escRotation);

  // Escape wheel rim & spokes
  ctx.strokeStyle = "#FBBF24";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(0, 0, escRadius, 0, Math.PI * 2);
  ctx.stroke();

  // 15 Club Teeth
  for (let i = 0; i < 15; i++) {
    const angle = (i * Math.PI * 2) / 15;
    ctx.save();
    ctx.rotate(angle);
    ctx.fillStyle = "#D4AF37";
    ctx.beginPath();
    ctx.moveTo(escRadius, 0);
    ctx.lineTo(escRadius + 14, 6);
    ctx.lineTo(escRadius + 10, -4);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }
  ctx.restore();

  // Middle: Pallet Fork (Pivot at X: 470, Y: 170)
  const forkPivotX = 490;
  const forkPivotY = 170;

  ctx.save();
  ctx.translate(forkPivotX, forkPivotY);
  ctx.rotate(fAngle);

  // Fork body
  ctx.strokeStyle = "#C58F7D";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-70, -25); // Entry arm
  ctx.moveTo(0, 0);
  ctx.lineTo(-70, 25);  // Exit arm
  ctx.moveTo(0, 0);
  ctx.lineTo(60, 0);    // Lever dart towards balance
  ctx.stroke();

  // Ruby Pallet Jewels
  ctx.fillStyle = "#FF5E7E";
  ctx.shadowColor = "#FF5E7E";
  ctx.shadowBlur = 8;
  ctx.fillRect(-76, -29, 8, 8);
  ctx.fillRect(-76, 21, 8, 8);
  ctx.shadowBlur = 0;
  ctx.restore();

  // Right side: Balance Wheel & Breguet Hairspring (Pivot at X: 720, Y: 170)
  const balX = 720;
  const balY = 170;
  const balRadius = 85;

  ctx.save();
  ctx.translate(balX, balY);
  ctx.rotate(bAngle);

  // Glucydur Balance Rim
  ctx.strokeStyle = "#FAF9F6";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(0, 0, balRadius, 0, Math.PI * 2);
  ctx.stroke();

  // Balance compensation regulation screws on rim
  ctx.fillStyle = "#D4AF37";
  for (let i = 0; i < 16; i++) {
    const sa = (i * Math.PI * 2) / 16;
    const sx = Math.cos(sa) * balRadius;
    const sy = Math.sin(sa) * balRadius;
    ctx.beginPath();
    ctx.arc(sx, sy, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  // 3 Balance Arms
  for (let i = 0; i < 3; i++) {
    const a = (i * Math.PI * 2) / 3;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(Math.cos(a) * balRadius, Math.sin(a) * balRadius);
    ctx.stroke();
  }

  // Breguet Hairspring (Archimedean Spiral)
  ctx.strokeStyle = "rgba(0, 229, 255, 0.6)";
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  const spiralTurns = 6;
  for (let theta = 0; theta < Math.PI * 2 * spiralTurns; theta += 0.1) {
    const r = (theta / (Math.PI * 2 * spiralTurns)) * 48;
    const x = Math.cos(theta + bAngle * 0.4) * r;
    const y = Math.sin(theta + bAngle * 0.4) * r;
    if (theta === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // Center Ruby Cap Jewel
  ctx.fillStyle = "#DC2626";
  ctx.beginPath();
  ctx.arc(0, 0, 8, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function playMechanicalTick(freq) {
  if (!soundEnabled) return;
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!audioCtx) audioCtx = new AudioContextClass();
  if (audioCtx.state === "suspended") audioCtx.resume();

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  const now = audioCtx.currentTime;

  osc.type = "sine";
  osc.frequency.setValueAtTime(freq, now);
  osc.frequency.exponentialRampToValueAtTime(800, now + 0.015);

  gain.gain.setValueAtTime(0.08, now);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.02);

  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(now);
  osc.stop(now + 0.025);
}

function setupAudioToggle() {
  const btn = document.getElementById("btn-sound-toggle");
  if (!btn) return;
  btn.addEventListener("click", () => {
    soundEnabled = !soundEnabled;
    btn.textContent = soundEnabled ? "🔊 TICK AUDIO: ON" : "🔇 TICK AUDIO: OFF";
    btn.style.color = soundEnabled ? "#D4AF37" : "#94A3B8";
  });
}

function setupVphSelector() {
  const btns = document.querySelectorAll(".btn-vph");
  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      btns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentVph = parseInt(btn.getAttribute("data-vph"), 10);
    });
  });
}

// 2. Macro Split-Screen Slider
function setupMacroSlider() {
  const container = document.getElementById("macro-slider-box");
  const afterView = document.getElementById("after-layer-view");
  const handle = document.getElementById("slider-divider");
  if (!container || !afterView || !handle) return;

  let isDragging = false;

  function updateSlider(clientX) {
    const rect = container.getBoundingClientRect();
    const offsetX = Math.max(0, Math.min(rect.width, clientX - rect.left));
    const pct = (offsetX / rect.width) * 100;

    afterView.style.width = pct + "%";
    handle.style.left = pct + "%";
  }

  container.addEventListener("mousedown", () => isDragging = true);
  window.addEventListener("mouseup", () => isDragging = false);
  window.addEventListener("mousemove", (e) => {
    if (isDragging) updateSlider(e.clientX);
  });

  container.addEventListener("click", (e) => updateSlider(e.clientX));
}

// 3. Order Tracking
function setupOrderTracking() {
  const btnTrack = document.getElementById("btn-track-order");
  const inputTrack = document.getElementById("track-id-input");

  btnTrack.addEventListener("click", () => {
    const id = inputTrack.value.trim();
    if (id) trackOrder(id);
  });

  inputTrack.addEventListener("keypress", (e) => {
    if (e.key === "Enter") btnTrack.click();
  });
}

async function trackOrder(orderId) {
  try {
    const res = await fetch(`/api/track-order/${orderId}`);
    const data = await res.json();
    if (data.found && data.order) {
      renderOrderDetails(data.order);
    }
  } catch (err) {
    console.error("Order tracking error:", err);
  }
}

function renderOrderDetails(order) {
  document.getElementById("res-watch-model").textContent = `${order.brand} (${order.caliber})`;
  document.getElementById("res-client-tag").textContent = `Клиент: ${order.client_name}`;
  document.getElementById("res-master-notes").textContent = order.master_notes;

  const timeline = document.getElementById("stages-timeline-list");
  timeline.innerHTML = order.stages.map((st, idx) => `
    <div class="stage-item">
      <div class="stage-status-dot ${st.status}"></div>
      <span class="stage-title">Этап ${idx + 1}: <strong>${st.title}</strong></span>
      <span class="stage-date">${st.date}</span>
    </div>
  `).join("");
}

// 4. Appraisal Form
function setupAppraisalForm() {
  const form = document.getElementById("appraisal-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      client_name: document.getElementById("ap-contact").value,
      client_contact: document.getElementById("ap-contact").value,
      watch_brand: document.getElementById("ap-brand").value,
      caliber: document.getElementById("ap-caliber").value || "Unknown",
      vintage_decade: document.getElementById("ap-decade").value,
      defect_description: document.getElementById("ap-defect").value
    };

    try {
      const res = await fetch("/api/appraisal-request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      const alertEl = document.getElementById("appraisal-alert");

      if (res.ok && data.status === "success") {
        alertEl.innerHTML = `
          ✅ <strong>${data.message}</strong><br>
          Номер тикета: <code>${data.appraisal.ticket_id}</code><br>
          Ориентировочная стоимость реставрации: <strong>${data.appraisal.estimate_range}</strong>
        `;
        alertEl.className = "appraisal-alert success";
        alertEl.classList.remove("hidden");
        form.reset();
      }
    } catch (err) {
      console.error("Appraisal error:", err);
    }
  });
}
