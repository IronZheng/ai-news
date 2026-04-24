const PROXIES = [
  (url) => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
  (url) => `https://corsproxy.io/?${encodeURIComponent(url)}`,
  (url) => `https://r.jina.ai/http://${url.replace(/^https?:\/\//, "")}`
];

async function tryFetch(url, parseAs = "text") {
  const errors = [];

  for (const proxy of PROXIES) {
    const proxiedUrl = proxy(url);
    try {
      const response = await fetch(proxiedUrl);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return parseAs === "json" ? response.json() : response.text();
    } catch (error) {
      errors.push(`${proxiedUrl} -> ${error.message}`);
    }
  }

  throw new Error(`All proxy requests failed. ${errors.join(" | ")}`);
}

export async function fetchTextViaProxy(url) {
  return tryFetch(url, "text");
}

export async function fetchJsonViaProxy(url) {
  return tryFetch(url, "json");
}
