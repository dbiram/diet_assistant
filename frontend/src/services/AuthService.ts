const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function login(username: string, password: string) {
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  if (!res.ok) {
    const { detail } = await res.json();
    throw new Error(detail || "Login failed");
  }

  const data = await res.json();
  return data.access_token;
}