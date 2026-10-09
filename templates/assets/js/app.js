/* Doctors of Natural Medicine — California
   Progressive enhancement only. The site is fully usable with JS disabled.
   No third-party scripts, no trackers, no PHI ever leaves the page. */
(function () {
  "use strict";

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  var backdrop;
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
      if (open) {
        backdrop = document.createElement("div");
        backdrop.className = "nav-backdrop";
        backdrop.addEventListener("click", closeNav);
        document.body.appendChild(backdrop);
      } else {
        closeNav();
      }
    });
  }
  function closeNav() {
    if (!nav) return;
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    if (backdrop && backdrop.parentNode) { backdrop.parentNode.removeChild(backdrop); backdrop = null; }
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeNav(); });

  /* ---------- Reduced-motion-aware reveal on scroll ---------- */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- State-selector memory (routing hint only; no PHI) ---------- */
  try {
    var saved = localStorage.getItem("dnm_state");
    if (saved) {
      var active = document.querySelector('.state-pill[data-state="' + saved + '"]');
      // purely cosmetic; do not auto-redirect
    }
    document.querySelectorAll(".state-pill").forEach(function (p) {
      p.addEventListener("click", function () {
        try { localStorage.setItem("dnm_state", p.textContent.trim().slice(0, 24)); } catch (e) {}
      });
    });
  } catch (e) {}

  var LAUNCH_MODE = document.body.getAttribute("data-launch-mode") !== "live";

  /* ---------- Booking router (pre-booking state question) ---------- */
  var router = document.getElementById("booking-router");
  if (router) {
    var out = router.querySelector("[data-router-output]");
    router.querySelectorAll("[data-route]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var route = btn.getAttribute("data-route");
        showRoute(route);
      });
    });
    function showRoute(route) {
      if (!out) return;
      var html = "";
      if (route === "ca-new" || route === "ca-renew") {
        if (LAUNCH_MODE) {
          html = '<div class="callout warn"><strong>Not yet booking.</strong> California evaluations have not launched. '
               + 'Join the launch list and we\u2019ll email you the moment California appointments open.'
               + '<p style="margin:.8rem 0 0"><a class="btn btn-primary btn-sm" href="#notify">Get launch updates</a></p></div>';
        } else {
          html = '<div class="callout"><strong>Great \u2014 let\u2019s continue.</strong> You\u2019ll confirm you are physically located in California inside our secure scheduling system. '
               + '<p style="margin:.8rem 0 0"><a class="btn btn-primary btn-sm" data-booking-cta href="#book-provider">Continue to secure booking</a></p></div>';
        }
      } else if (route === "co") {
        html = '<div class="callout"><strong>You\u2019re looking for Colorado care.</strong> Our Colorado clinics handle in\u2011clinic and telehealth evaluations. '
             + '<p style="margin:.8rem 0 0"><a class="btn btn-secondary btn-sm" href="https://drnatmed.com/appointment/">Go to Colorado booking</a></p></div>';
      } else if (route === "question") {
        html = '<div class="callout"><strong>Happy to help.</strong> Use the contact options below \u2014 these are public inquiries only, so please don\u2019t include medical details. '
             + '<p style="margin:.8rem 0 0"><a class="btn btn-ghost btn-sm" href="/california/contact/">Contact &amp; support</a></p></div>';
      } else if (route === "physician") {
        html = '<div class="callout"><strong>You\u2019re a clinician.</strong> See how the clinical work operates and start an inquiry. '
             + '<p style="margin:.8rem 0 0"><a class="btn btn-ghost btn-sm" href="/careers/california-physicians/">For physicians</a></p></div>';
      }
      out.innerHTML = html;
      out.hidden = false;
      bindBookingCta();
      out.setAttribute("tabindex", "-1");
      out.focus();
    }
  }

  /* ---------- Demo booking adapter (NEVER confirms a real appointment) ---------- */
  function bindBookingCta() {
    document.querySelectorAll("[data-booking-cta]").forEach(function (cta) {
      if (cta.__bound) return; cta.__bound = true;
      cta.addEventListener("click", function (e) {
        e.preventDefault();
        alert(
          "DEMO BOOKING ADAPTER\n\n" +
          "This preview is not connected to a live scheduling system, so no appointment " +
          "has been booked and no payment has been taken.\n\n" +
          "Before launch, this button routes to the approved, BAA-covered scheduling vendor " +
          "where you confirm your California location and complete secure intake."
        );
      });
    });
  }
  bindBookingCta();

  /* ---------- Public inquiry / notify / recruitment forms ---------- *
   * Public forms collect MINIMAL contact info only. They never collect
   * diagnoses, medical history, or ID documents. In preview there is no
   * endpoint, so we show an explicit "not transmitted" message.           */
  document.querySelectorAll("form[data-public-form]").forEach(function (form) {
    var msg = form.querySelector(".form-msg");
    form.setAttribute("novalidate", "novalidate");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      clearErrors(form);
      var ok = validate(form);
      if (!ok) {
        if (msg) { msg.hidden = false; msg.className = "form-msg err"; msg.textContent = "Please fix the highlighted fields and try again."; }
        var firstErr = form.querySelector('[aria-invalid="true"]');
        if (firstErr) firstErr.focus();
        return;
      }
      var endpoint = form.getAttribute("data-endpoint") || "";
      if (!endpoint || endpoint.indexOf("TODO") === 0) {
        // Preview: do not transmit anything.
        if (msg) {
          msg.hidden = false; msg.className = "form-msg ok";
          msg.textContent = "Preview mode: your details were NOT sent anywhere. Configure an approved form endpoint before launch.";
        }
        form.reset();
        return;
      }
      // Live mode would POST minimal fields here with fetch(); omitted in preview.
      if (msg) { msg.hidden = false; msg.className = "form-msg ok"; msg.textContent = "Thank you \u2014 we\u2019ve received your request and will be in touch."; }
      form.reset();
    });
  });

  function validate(form) {
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (f) {
      var val = (f.value || "").trim();
      var valid = val.length > 0;
      if (f.type === "email") valid = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val);
      if (f.type === "checkbox") valid = f.checked;
      if (!valid) { setError(f, f.getAttribute("data-error") || "This field is required."); ok = false; }
    });
    return ok;
  }
  function setError(field, text) {
    field.setAttribute("aria-invalid", "true");
    var id = field.getAttribute("aria-describedby");
    if (id) { var e = document.getElementById(id); if (e) e.textContent = text; }
  }
  function clearErrors(form) {
    if (form.querySelector(".form-msg")) form.querySelector(".form-msg").hidden = true;
    form.querySelectorAll('[aria-invalid="true"]').forEach(function (f) {
      f.removeAttribute("aria-invalid");
      var id = f.getAttribute("aria-describedby");
      if (id) { var e = document.getElementById(id); if (e) e.textContent = ""; }
    });
  }
})();
