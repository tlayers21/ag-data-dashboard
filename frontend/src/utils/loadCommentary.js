export async function loadCommentary() {
  try {
    const API = process.env.REACT_APP_API_BASE || "";
    const ROOT = API.replace("/api", "");

    const res = await fetch(`${ROOT}/commentary/home`);
    const text = await res.text();

    const paragraphs = text.split(/\n\s*\n/).filter(Boolean);

    const groups = {
      corn: [],
      soybeans: [],
      wheat: []
    };

    for (const p of paragraphs) {
      const lower = p.toLowerCase();
      if (lower.includes("corn")) {
        groups.corn.push(p.replace(/^JAN-\d{1,2}:\s*/, ""));
      } else if (lower.includes("soybeans")) {
        groups.soybeans.push(p.replace(/^JAN-\d{1,2}:\s*/, ""));
      } else if (lower.includes("wheat")) {
        groups.wheat.push(p.replace(/^JAN-\d{1,2}:\s*/, ""));
      }
    }

    for (const key of Object.keys(groups)) {
      if (groups[key].length > 0) {
        groups[key][0] = `<strong>JAN-14:</strong> ${groups[key][0]}`;
      }
    }

    return groups;
  } catch (err) {
    console.error("Commentary load failed:", err);
    return {
      corn: [],
      soybeans: [],
      wheat: []
    };
  }
}