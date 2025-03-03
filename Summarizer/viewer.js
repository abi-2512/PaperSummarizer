window.addEventListener("DOMContentLoaded", async () => {
    // Get the PDF file URL from the query string, e.g. ?file=https://example.com/my.pdf
    const params = new URLSearchParams(window.location.search);
    const pdfUrl = params.get("file");
    if (!pdfUrl) {
      document.body.textContent = "No PDF file specified.";
      return;
    }
    
    // Set up PDF.js worker
    pdfjsLib.GlobalWorkerOptions.workerSrc = "pdfjs/pdf.worker.js";
    
    try {
      const loadingTask = pdfjsLib.getDocument(pdfUrl);
      const pdf = await loadingTask.promise;
      // For example, render the first page
      const page = await pdf.getPage(1);
      const viewport = page.getViewport({ scale: 1.5 });
      const canvas = document.getElementById("pdf-canvas");
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      const context = canvas.getContext("2d");
      const renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      await page.render(renderContext).promise;
    } catch (error) {
      console.error("Error loading PDF:", error);
      document.body.textContent = "Error loading PDF.";
    }
  });
  