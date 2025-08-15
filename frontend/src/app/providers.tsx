'use client';

import { AuthProvider } from '@/contexts/AuthContext';
import { ToastContainer } from 'react-toastify';
import Navbar from '@/components/Navbar';

export function Providers({ 
  children 
}: { 
  children: React.ReactNode 
}) {
  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow">
          {children}
        </main>
        <footer className="py-6 text-center bg-white border-t">
          <p className="text-sm text-gray-500">© {new Date().getFullYear()} SnapWave. All rights reserved.</p>
        </footer>
        <ToastContainer position="top-right" autoClose={5000} />
      </div>
    </AuthProvider>
  );
}
