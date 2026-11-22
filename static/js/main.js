/**
 * Global UI helper functions: modal windows, toast alerts,
 * and 3D origami paper-fold sidebar collapse / unfold animation.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Modal handlers (Supports both .open and .active)
  document.querySelectorAll("[data-modal-open]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const modalId = btn.getAttribute("data-modal-open");
      const target = document.getElementById(modalId);
      if (target) {
        target.classList.add("open");
        target.classList.add("active");
      }
    });
  });

  document.querySelectorAll("[data-modal-close]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const modal = btn.closest(".modal-backdrop");
      if (modal) {
        modal.classList.remove("open");
        modal.classList.remove("active");
      }
    });
  });

  // Client-side quick filter for tables
  const quickSearch = document.getElementById("tableSearchInput");
  if (quickSearch) {
    quickSearch.addEventListener("keyup", (e) => {
      const query = e.target.value.toLowerCase();
      const rows = document.querySelectorAll(".filterable-row");
      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? "" : "none";
      });
    });
  }

  // 3D Origami Paper Fold Sidebar Collapse / Unfold Handler
  const appContainer = document.querySelector(".app-container");
  const toggleBtn = document.getElementById("sidebarToggleBtn");
  const overlay = document.getElementById("sidebarOverlay");

  function toggleSidebar() {
    if (!appContainer) return;

    if (window.innerWidth <= 768) {
      appContainer.classList.toggle("sidebar-mobile-open");
    } else {
      appContainer.classList.add("sidebar-animating");
      appContainer.classList.toggle("sidebar-collapsed");
      const isCollapsed = appContainer.classList.contains("sidebar-collapsed");
      try {
        localStorage.setItem("sidebar_collapsed", isCollapsed ? "1" : "0");
      } catch (err) {}
      setTimeout(() => {
        appContainer.classList.remove("sidebar-animating");
      }, 420);
    }
  }

  if (toggleBtn) toggleBtn.addEventListener("click", toggleSidebar);
  if (overlay) {
    overlay.addEventListener("click", () => {
      if (appContainer) appContainer.classList.remove("sidebar-mobile-open");
    });
  }

  // Restore saved desktop state
  try {
    if (window.innerWidth > 768 && localStorage.getItem("sidebar_collapsed") === "1") {
      if (appContainer) appContainer.classList.add("sidebar-collapsed");
    }
  } catch (err) {}

  // Auto-dismiss alerts after 6 seconds
  document.querySelectorAll(".flash-alert").forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      alert.style.opacity = "0";
      alert.style.transform = "translateY(-4px)";
      setTimeout(() => alert.remove(), 400);
    }, 6000);
  });
});
