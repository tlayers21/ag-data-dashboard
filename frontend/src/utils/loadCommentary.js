export async function loadCommentary(files) {
  const texts = await Promise.all(
    files.map((file) => fetch(file).then((r) => r.text()))
  );

  return texts.join("\n\n");
}