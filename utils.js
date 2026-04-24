export function hashString(value) {
  let hash = 0;
  for (let i = 0; i < value.length; i += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(i);
    hash |= 0;
  }
  return String(hash);
}

export function parseDate(value) {
  const date = value ? new Date(value) : null;
  return date && !Number.isNaN(date.getTime()) ? date : null;
}

export function formatDate(value) {
  const date = typeof value === "string" ? parseDate(value) : value;
  if (!date) {
    return "Unknown time";
  }

  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
}

export function isRecent(date, days = 7) {
  if (!(date instanceof Date)) {
    return false;
  }

  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  return date.getTime() >= cutoff;
}

export function normalizeText(value) {
  return (value || "").replace(/\s+/g, " ").trim();
}

export function decodeHtmlEntities(value) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(value || "", "text/html");
  return doc.documentElement.textContent || "";
}

export function stripHtml(value) {
  return decodeHtmlEntities((value || "").replace(/<[^>]*>/g, " "));
}
