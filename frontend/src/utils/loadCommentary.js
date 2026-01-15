const API = process.env.REACT_APP_API_BASE;
const ROOT = API.replace("/api", "");

export async function loadCommentary() {
  const res = await fetch(`${ROOT}/commentary/home`);
  let text = await res.text();

  // Split on double newlines (your backend uses \n\n between items)
  let parts = text.split(/\n\s*\n/).filter(Boolean);

  if (parts.length === 0) return "";

  // Bold the first date prefix in the first item
  parts[0] = parts[0].replace(
    /^([A-Z]{3}-\d{1,2}:)/,
    "<strong>$1</strong>"
  );

  // Strip date prefixes from all subsequent items
  for (let i = 1; i < parts.length; i++) {
    parts[i] = parts[i].replace(/^[A-Z]{3}-\d{1,2}:\s*/, "");
  }

  // Join into one paragraph
  return parts.join(" ");
}