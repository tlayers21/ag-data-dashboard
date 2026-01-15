export async function loadCommentary() {
  const res = await fetch(`${process.env.REACT_APP_API_BASE}/commentary/home`);
  const text = await res.text();
  return text;
}