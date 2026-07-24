import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/authService.ts";

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");

    try {
      setLoading(true);

      const data = await login(email, password);

        localStorage.setItem(
        "access_token",
        data.access_token
      );

      navigate("/dashboard");

    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Login failed."
      );
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-5">

      <div>
        <label className="block mb-2 font-medium">
          Email Address
        </label>

        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>

        <div className="flex justify-between mb-2">

          <label className="font-medium">
            Password
          </label>

          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="text-sm text-blue-600"
          >
            {showPassword ? "Hide" : "Show"}
          </button>

        </div>

        <input
          type={showPassword ? "text" : "password"}
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

      </div>

      {error && (
      <p className="text-sm text-red-600">
          {error}
      </p>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
            {loading ? "Logging in..." : "Login"}
        </button>

    </form>
  );
}

export default LoginForm;