document.getElementById("openCustomViewer").addEventListener("click", async () => {
  // Assume you get the current tab's URL (the PDF URL)
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.url) {
    // Open your custom viewer with the PDF URL as a parameter
    const viewerUrl = chrome.runtime.getURL("viewer.html") + "?file=" + encodeURIComponent(tab.url);
    chrome.tabs.create({ url: viewerUrl });
  }
});

  
  // Execute the extraction function in the active tab.
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: extractPDFTextFromPage,
  }, async (results) => {
    if (chrome.runtime.lastError) {
      document.getElementById("summary").innerText =
        "Error: " + chrome.runtime.lastError.message;
      return;
    }
    if (results && results[0] && results[0].result) {
      const pdfText = results[0].result;
      document.getElementById("summary").innerText =
        "Extracted PDF text (first 200 chars):\n" +
        pdfText.substring(0, 200) +
        "\n\nSending to Flask...";
      
      // Send extracted text to Flask.
      try {
        const response = await fetch("http://127.0.0.1:5000/summarize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: pdfText })
        });
        const data = await response.json();
        document.getElementById("summary").innerText = "Summary:\n" + data.summary;
      } catch (error) {
        document.getElementById("summary").innerText =
          "Error sending to Flask: " + error.message;
      }
    } else {
      document.getElementById("summary").innerText = "Failed to extract PDF text.";
    }
  });

/**
 * This function runs in the context of the active tab (i.e. the PDF page).
 * It waits for pdfjsLib to be defined (polling for up to 5 seconds) before proceeding.
 */
async function extractPDFTextFromPage() {
  // Define a helper function that polls for pdfjsLib.
  async function waitForPDFjsLib(timeout = 5000) {
    return new Promise((resolve, reject) => {
      const interval = 100; // check every 100ms
      let elapsed = 0;
      const timer = setInterval(() => {
        if (window.pdfjsLib) {
          clearInterval(timer);
          resolve(window.pdfjsLib);
        } else {
          elapsed += interval;
          if (elapsed >= timeout) {
            clearInterval(timer);
            reject(new Error("pdfjsLib not found after waiting"));
          }
        }
      }, interval);
    });
  }
  
  // Wait until pdfjsLib is available.
  try {
    await waitForPDFjsLib();
  } catch (error) {
    console.error(error);
    return "";
  }
  
  // Set the worker source for PDF.js.
  window.pdfjsLib.GlobalWorkerOptions.workerSrc = chrome.runtime.getURL("pdfjs/pdf.worker.js");
  const pdfUrl = window.location.href;
  try {
    const loadingTask = window.pdfjsLib.getDocument(pdfUrl);
    const pdf = await loadingTask.promise;
    let fullText = "";
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      fullText += textContent.items.map(item => item.str).join(" ") + "\n";
    }
    return fullText;
  } catch (error) {
    console.error("Error extracting PDF:", error);
    return "";
  }
}
