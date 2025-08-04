import { useEffect, useState } from "react";
import { getProfile, saveProfile } from "../services/ProfileService";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export default function ProfilePage() {
  const { token } = useAuth();
  const [profile, setProfile] = useState({
    age: "",
    gender: "",
    weight_kg: "",
    height_cm: "",
    activity_level: "",
    target_weight_kg: "",
    timeframe_weeks: "",
    workouts_per_week: ""
  });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

useEffect(() => {
    async function fetchData() {
      try {
        const data = await getProfile(token!);
        const {
          age, gender, weight_kg, height_cm,
          activity_level, target_weight_kg,
          timeframe_weeks, workouts_per_week
        } = data;

        setProfile({
          age: age.toString(),
          gender,
          weight_kg: weight_kg.toString(),
          height_cm: height_cm.toString(),
          activity_level,
          target_weight_kg: target_weight_kg.toString(),
          timeframe_weeks: timeframe_weeks.toString(),
          workouts_per_week: workouts_per_week.toString(),
        });
      } catch (err) {
        console.error(err);
        setMessage("No profile found. Please fill in your information.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [token]);

  const handleChange = (e: { target: { name: any; value: any; }; }) => {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    const payload = {
      ...profile,
      age: parseInt(profile.age),
      weight_kg: parseFloat(profile.weight_kg),
      height_cm: parseFloat(profile.height_cm),
      target_weight_kg: parseFloat(profile.target_weight_kg),
      timeframe_weeks: parseInt(profile.timeframe_weeks),
      workouts_per_week: parseInt(profile.workouts_per_week),
    };

    try {
      await saveProfile(token!, payload);
      setMessage("Profile saved successfully!");
    } catch (err) {
      setMessage("Error saving profile.");
    }
  };

  if (loading) return <div className="p-4">Loading profile...</div>;

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold">Your Profile</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="age">Age</label>
          <Input name="age" id="age" placeholder="Age" value={profile.age} onChange={handleChange} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="gender">Gender</label>
          <select
            name="gender"
            id="gender"
            value={profile.gender}
            onChange={handleChange}
            className="w-full p-2 border rounded-md text-sm"
          >
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="weight_kg">Weight (kg)</label>
          <Input name="weight_kg" id="weight_kg" placeholder="Weight in kg" value={profile.weight_kg} onChange={handleChange} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="height_cm">Height (cm)</label>
          <Input name="height_cm" id="height_cm" placeholder="Height in cm" value={profile.height_cm} onChange={handleChange} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="activity_level">Activity Level</label>
          <select
            name="activity_level"
            id="activity_level"
            value={profile.activity_level}
            onChange={handleChange}
            className="w-full p-2 border rounded-md text-sm"
          >
            <option value="">Select activity level</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="target_weight_kg">Target Weight (kg)</label>
          <Input name="target_weight_kg" id="target_weight_kg" placeholder="Target weight" value={profile.target_weight_kg} onChange={handleChange} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="timeframe_weeks">Timeframe (weeks)</label>
          <Input name="timeframe_weeks" id="timeframe_weeks" placeholder="How many weeks?" value={profile.timeframe_weeks} onChange={handleChange} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="workouts_per_week">Workouts per week</label>
          <Input name="workouts_per_week" id="workouts_per_week" placeholder="e.g. 3" value={profile.workouts_per_week} onChange={handleChange} />
        </div>

        <Button type="submit" className="mt-2">Save Profile</Button>
        {message && <p className="text-sm text-center text-green-600">{message}</p>}
      </form>
    </div>
  );
}