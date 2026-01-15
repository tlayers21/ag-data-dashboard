export async function loadCommentary() {
  try {
    const API = process.env.REACT_APP_API_BASE || "";
    const ROOT = API.replace("/api", "");

    const res = await fetch(`${ROOT}/commentary/home`);
    let text = await res.text();

    // Fix escaped newlines and stray quotes
    text = text.replace(/\\n/g, "\n").replace(/^"+|"+$/g, "");

    // Split into paragraphs
    const paragraphs = text.split(/\n\s*\n/).filter(Boolean);

    const groups = {
      corn: [],
      soybeans: [],
      wheat: []
    };

    const dateRegex = /^([A-Z]{3}-\d{1,2}):\s*/;

    for (let p of paragraphs) {
      p = p.trim();

      // Strip leading/trailing quotes on each paragraph
      p = p.replace(/^"+|"+$/g, "");

      const match = p.match(dateRegex);
      const datePrefix = match ? match[1] : null;
      const cleaned = p.replace(dateRegex, "");

      const lower = p.toLowerCase();

      if (lower.includes("corn")) {
        groups.corn.push({ date: datePrefix, text: cleaned });
      } else if (lower.includes("soybeans")) {
        groups.soybeans.push({ date: datePrefix, text: cleaned });
      } else if (lower.includes("wheat")) {
        groups.wheat.push({ date: datePrefix, text: cleaned });
      }
    }

    // Helper to order sentences within a commodity
    const orderSentences = (items) => {
      const buckets = {
        inspections: null,
        total: null,
        gross: null,
        next: null
      };

      for (const item of items) {
        const t = item.text.toLowerCase();
        if (t.includes("export inspections")) buckets.inspections = item.text;
        else if (t.includes("current marketing year total commitment")) buckets.total = item.text;
        else if (t.includes("gross new sales")) buckets.gross = item.text;
        else if (t.includes("next marketing year outstanding sales")) buckets.next = item.text;
      }

      return [buckets.inspections, buckets.total, buckets.gross, buckets.next]
        .filter(Boolean);
    };

    const buildBlock = (items) => {
      if (items.length === 0) return "";

      const date = items[0].date || "";
      const ordered = orderSentences(items);

      // First sentence keeps the date, others drop it
      const first = ordered[0];
      const rest = ordered.slice(1).map(s =>
        s.replace(dateRegex, "").trim()
      );

      const body = [first.replace(dateRegex, "").trim(), ...rest].join(" ");

      return `<strong>${date}:</strong> ${body}`;
    };

    return {
      corn: buildBlock(groups.corn),
      soybeans: buildBlock(groups.soybeans),
      wheat: buildBlock(groups.wheat)
    };

  } catch (err) {
    console.error("Commentary load failed:", err);
    return { corn: "", soybeans: "", wheat: "" };
  }
}