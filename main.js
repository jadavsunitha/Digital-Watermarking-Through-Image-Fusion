document.addEventListener("DOMContentLoaded", () => {
  
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
      form.addEventListener("submit", () => {
        document.getElementById("spinner").classList.remove("hidden");
      });
    });
  });
  
  function showStatus(message) {
    const msgBox = document.getElementById("status-message");
    msgBox.textContent = message;
    msgBox.classList.remove("hidden");
    setTimeout(() => msgBox.classList.add("hidden"), 3000);
  }
  