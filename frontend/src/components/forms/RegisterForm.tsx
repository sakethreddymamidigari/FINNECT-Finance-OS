function RegisterForm() {
  return (
    <form className="space-y-5">

      <div>
        <label className="block mb-2 font-medium">
          Finance Name
        </label>

        <input
          type="text"
          placeholder="Enter finance name"
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block mb-2 font-medium">
          Owner Name
        </label>

        <input
          type="text"
          placeholder="Enter owner name"
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block mb-2 font-medium">
          Email Address
        </label>

        <input
          type="email"
          placeholder="Enter email"
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block mb-2 font-medium">
          Mobile Number
        </label>

        <input
          type="tel"
          placeholder="Enter mobile number"
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block mb-2 font-medium">
          Password
        </label>

        <input
          type="password"
          placeholder="Enter password"
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block mb-2 font-medium">
          Confirm Password
        </label>

        <input
          type="password"
          placeholder="Confirm password"
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition"
      >
        Register
      </button>

    </form>
  );
}

export default RegisterForm;