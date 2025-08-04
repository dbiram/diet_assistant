const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getProfile(token: string) {
  const res = await fetch(`${BASE_URL}/profile/my_profile`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) throw new Error("Failed to fetch profile");

  return res.json();
}

export async function saveProfile(token: string, data: any) {
  const res = await fetch(`${BASE_URL}/profile/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Failed to save profile");

  return res.json();
}
