const PROXIES = [
  {
    name: "codetabs",
    buildUrl: (url) => `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`
  },
  {
    name: "allorigins",
    buildUrl: (url) => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`
  }
];

async function parseResponse(response, parseAs) {
  if (parseAs === "json") {
    const text = await response.text();
    return JSON.parse(text);
  }
  return response.text();
}

async function fetchDirect(url, parseAs) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return parseResponse(response, parseAs);
}

async function fetchViaProxies(url, parseAs) {
  const errors = [];

  for (const proxy of PROXIES) {
    const proxiedUrl = proxy.buildUrl(url);
    try {
      const response = await fetch(proxiedUrl);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await parseResponse(response, parseAs);
    } catch (error) {
      errors.push(`${proxy.name}: ${error.message}`);
    }
  }

  throw new Error(`All proxy requests failed for ${url}. ${errors.join(" | ")}`);
}

async function fetchResilient(url, parseAs) {
  try {
    return await fetchDirect(url, parseAs);
  } catch (directError) {
    return fetchViaProxies(url, parseAs);
  }
}

export async function fetchTextResilient(url) {
  return fetchResilient(url, "text");
}

export async function fetchJsonResilient(url) {
  return fetchResilient(url, "json");
}
