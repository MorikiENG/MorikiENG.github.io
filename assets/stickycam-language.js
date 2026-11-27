/* Only the common language-entry page redirects; policy pages stay on the chosen language. */
(() => {
  const preferred = Array.from(navigator.languages || [navigator.language || "ja"]);
  const match = preferred.map(value => value.toLowerCase().split("-")[0]).find(value => value === "ja" || value === "en");
  const language = match || "ja";
  const link = document.querySelector('[data-language="' + language + '"]');
  if (link) window.location.replace(link.href);
})();
