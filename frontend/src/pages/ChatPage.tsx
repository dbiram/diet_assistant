import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { sendChatMessage } from "../services/ChatService";
import { estimateNutritionFromImage, logMeal } from "../services/NutritionService";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export default function ChatPage() {
  const { token } = useAuth();
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);

  const [, setImage] = useState<File | null>(null);
  const [imagePreviewUrl, ] = useState<string | null>(null);
  const [imageResult, setImageResult] = useState<{
    label: string;
    nutrition: {
      calories: number | "unknown";
      protein: number | "unknown";
      fat?: number | "unknown";
    };
  } | null>(null);
  const [loadingImage, setLoadingImage] = useState(false);

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingChat(true);
    setChatResponse("");

    try {
      const data = await sendChatMessage(token!, message);
      setChatResponse(data.response);
    } catch (err: any) {
      setChatResponse(err.message || "Error processing chat.");
    } finally {
      setLoadingChat(false);
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setImage(file);
    setImageResult(null);
    setLoadingImage(true);

    try {
      const data = await estimateNutritionFromImage(token!, file);
      setImageResult(data);
    } catch (err) {
      console.error(err);
      setImageResult(null);
    } finally {
      setLoadingImage(false);
    }
  };

  const handleLogImageMeal = async () => {
    if (
      !imageResult ||
      imageResult.nutrition.calories === "unknown" ||
      imageResult.nutrition.protein === "unknown"
    )
      return;
    try {
      await logMeal(token!, {
        food_name: imageResult.label,
        calories: imageResult.nutrition.calories,
        protein: imageResult.nutrition.protein,
      });
      alert("Meal logged!");
    } catch (err) {
      alert("Failed to log meal.");
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold">Diet Assistant</h1>

      {/* Chat prompt */}
      <form onSubmit={handleChatSubmit} className="space-y-2">
        <Input
          placeholder="Ask a question or log a meal..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <Button type="submit" disabled={loadingChat}>
          {loadingChat ? "Thinking..." : "Send"}
        </Button>
      </form>

      {chatResponse && (
        <div className="bg-gray-50 p-3 rounded-md shadow">
          <strong>Assistant:</strong>
          <p>{chatResponse}</p>
        </div>
      )}

      {/* Image upload + nutrition preview */}
      <div className="space-y-3">
        <label className="text-sm font-medium">Upload a food image</label>
        <Input type="file" accept="image/*" onChange={handleImageUpload} />

        {loadingImage && <p className="text-sm text-gray-500">Analyzing image...</p>}

        {imagePreviewUrl && (
          <img
            src={imagePreviewUrl}
            alt="Uploaded preview"
            className="max-w-full h-auto rounded-md border"
          />
        )}

        {imageResult && (
          <div className="bg-white border p-4 rounded-md space-y-2 shadow-sm">
            <p><strong>Detected:</strong> {imageResult.label}</p>
            <p><strong>Calories:</strong> {imageResult.nutrition.calories}</p>
            <p><strong>Protein:</strong> {imageResult.nutrition.protein}</p>
            {imageResult.nutrition.fat && (
              <p><strong>Fat:</strong> {imageResult.nutrition.fat}</p>
            )}

            {(imageResult.nutrition.calories === "unknown" ||
              imageResult.nutrition.protein === "unknown") ? (
              <p className="text-sm text-red-500">
                ⚠️ Nutrition not available — cannot log this meal.
              </p>
            ) : (
              <Button variant="outline" onClick={handleLogImageMeal}>
                Log this meal
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
