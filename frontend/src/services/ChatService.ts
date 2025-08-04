const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function sendChatMessage(token: string, prompt: string) {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!res.ok) {
    const { detail } = await res.json();
    throw new Error(detail || "Chat failed");
  }

  return res.json(); 
}
