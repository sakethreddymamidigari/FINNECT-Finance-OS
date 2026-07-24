import type { ReactNode } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

type MainLayoutProps = {
  children: ReactNode;
};

function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <main className="p-6 bg-slate-100 min-h-[calc(100vh-64px)]">
          {children}
        </main>

      </div>

    </div>
  );
}

export default MainLayout;