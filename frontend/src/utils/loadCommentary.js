export async function loadCommentary() {
  try {
    const API = process.env.REACT_APP_API_BASE || "";
    const ROOT = API.replace("/api", "");

    const res = await fetch(`${ROOT}/commentary/home`);
    const text = await res.text();

    // Split into paragraphs on blank lines
    let parts = text.split(/\n\s*\n/).filter(Boolean);

    const cleaned = parts.map((p, idx) => {
      // Bold the first date prefix (e.g., JAN-14:)
      if (idx === 0) {
        return p.replace(
          /^([A-Z]{3}-\d{1,2}:)/,
          "<strong>$1</strong>"
        );
      }

      // Remove repeated date prefixes for subsequent paragraphs
      return p.replace(/^[A-Z]{3}-\d{1,2}:\s*/, "");
    });

    // Join paragraphs with <br><br>
    return cleaned.join("<br><br>");
  } catch (err) {
    console.error("Commentary load failed:", err);
    return "Commentary unavailable.";
  }
}