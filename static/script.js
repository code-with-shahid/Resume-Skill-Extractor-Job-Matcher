document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.querySelector(".upload-box");
  const fileInput = document.querySelector('input[type="file"]');
  const form = document.querySelector("form");

  // Highlight on drag over
  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.borderColor = "#00e6e6";
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.style.borderColor = "#444";
  });

  // Handle file drop
  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.style.borderColor = "#444";
    fileInput.files = e.dataTransfer.files;
    dropArea.querySelector(".upload-label").innerText = fileInput.files[0].name;
  });

  // File chosen via input
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      dropArea.querySelector(".upload-label").innerText = fileInput.files[0].name;
    }
  });

  // Show loading alert
  form.addEventListener("submit", () => {
    alert("Uploading resume and matching... Please wait.");
  });
});
