export async function loadCommentary() {
  try {
    const API = process.env.REACT_APP_API_BASE || "";
    const ROOT = API.replace("/api", "");

    const res = await fetch(`${ROOT}/commentary/home`);
    let text = await res.text();

    text = text.replace(/\\n/g, "\n");

    const paragraphs = text.split(/\n\s*\n/).filter(Boolean);

    const groups = {
      corn: [],
      soybeans: [],
      wheat: []
    };

    for (const p of paragraphs) {
      const lower = p.toLowerCase();

      if (lower.includes("corn")) {
        groups.corn.push(p);
      } else if (lower.includes("soybeans")) {
        groups.soybeans.push(p);
      } else if (lower.includes("wheat")) {
        groups.wheat.push(p);
      }
    }

    return groups;

  } catch (err) {
    console.error("Commentary load failed:", err);
    return { corn: [], soybeans: [], wheat: [] };
  }
}