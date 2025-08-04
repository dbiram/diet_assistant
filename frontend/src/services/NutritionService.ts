const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function estimateNutritionFromImage(token: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/api/estimate_nutrition_from_image`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to estimate nutrition");

  return res.json(); // { label, nutrition: { calories, protein } }
}

export async function logMeal(token: string, data: { food_name: string; calories: number; protein: number }) {
  const res = await fetch(`${BASE_URL}/api/log_meal`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Failed to log meal");

  return res.json();
}
