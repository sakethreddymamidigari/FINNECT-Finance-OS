function Sidebar() {
  return (
    <aside className="w-64 bg-blue-700 text-white min-h-screen">

      <div className="h-16 flex items-center justify-center border-b border-blue-600">
        <h1 className="text-xl font-bold">
          FINNECT
        </h1>
      </div>

      <nav className="p-4 space-y-2">

        <button className="w-full text-left px-4 py-3 rounded hover:bg-blue-600">
          Dashboard
        </button>

        <button className="w-full text-left px-4 py-3 rounded hover:bg-blue-600">
          Customers
        </button>

        <button className="w-full text-left px-4 py-3 rounded hover:bg-blue-600">
          Loans
        </button>

        <button className="w-full text-left px-4 py-3 rounded hover:bg-blue-600">
          Payments
        </button>

        <button className="w-full text-left px-4 py-3 rounded hover:bg-blue-600">
          Renewals
        </button>

        <button className="w-full text-left px-4 py-3 rounded hover:bg-blue-600">
          Settings
        </button>

      </nav>

    </aside>
  );
}

export default Sidebar;