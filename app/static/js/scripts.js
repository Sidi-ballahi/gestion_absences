// Main JavaScript for the application

// Toggle the side navigation
window.addEventListener("DOMContentLoaded", (event) => {
  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector("#sidebarToggle")
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", (event) => {
      event.preventDefault()
      document.body.classList.toggle("sb-sidenav-toggled")
      localStorage.setItem("sb|sidebar-toggle", document.body.classList.contains("sb-sidenav-toggled"))
    })
  }

  // Add active class to current nav item
  const currentPath = window.location.pathname
  const navLinks = document.querySelectorAll(".nav-link")

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active")

      // If it's in a collapse, expand the collapse
      const collapseParent = link.closest(".collapse")
      if (collapseParent) {
        collapseParent.classList.add("show")
        const collapseToggle = document.querySelector(`[data-bs-target="#${collapseParent.id}"]`)
        if (collapseToggle) {
          collapseToggle.classList.remove("collapsed")
          collapseToggle.setAttribute("aria-expanded", "true")
        }
      }
    }
  })

  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Initialize toasts
  const toastElList = [].slice.call(document.querySelectorAll(".toast"))
  toastElList.map((toastEl) =>
    new bootstrap.Toast(toastEl, {
      autohide: true,
      delay: 5000,
    }).show(),
  )

  // Dark mode toggle
  const darkModeToggle = document.createElement("div")
  darkModeToggle.className = "dark-mode-toggle"
  darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>'
  document.body.appendChild(darkModeToggle)

  // Check for saved dark mode preference
  const darkMode = localStorage.getItem("darkMode") === "true"
  if (darkMode) {
    document.body.classList.add("dark-mode")
    darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>'
  }

  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode")
    const isDarkMode = document.body.classList.contains("dark-mode")
    localStorage.setItem("darkMode", isDarkMode)
    darkModeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>'
  })
})
