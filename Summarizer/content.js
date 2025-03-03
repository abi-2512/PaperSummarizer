console.log("Content script loaded on PDF page.");

// Inject the legacy pdf.js into the page if not already injected.
(function injectPDFJS() {
  if (!document.getElementById("pdfjs_injected")) {
    const script = document.createElement("script");
    script.id = "pdfjs_injected";
    // Ensure that pdf.js in your pdfjs folder is the legacy (non‑module) build.
    script.src = chrome.runtime.getURL("pdfjs/pdf.js");
    script.onload = () => {
      console.log("pdf.js injected into page context.");
    };
    (document.head || document.documentElement).appendChild(script);
  }
})();
