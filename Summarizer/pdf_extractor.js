// pdf_extractor.js

// Configure pdf.js to use the bundled worker.
// Ensure pdf.worker.js is also in your extension folder.
pdfjsLib.GlobalWorkerOptions.workerSrc = chrome.runtime.getURL('Summarizer/pdfjs/pdf.worker.js');

/**
 * Extracts text from a PDF given its URL.
 * @param {string} pdfUrl - The URL of the PDF.
 * @returns {Promise<string>} - The extracted text.
 */
async function extractPdfText(pdfUrl) {
  try {
    const loadingTask = pdfjsLib.getDocument(pdfUrl);
    const pdf = await loadingTask.promise;
    let fullText = "";
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map(item => item.str).join(" ");
      fullText += pageText + "\n";
    }
    return fullText;
  } catch (error) {
    console.error("Error extracting PDF text:", error);
    throw error;
  }
}
