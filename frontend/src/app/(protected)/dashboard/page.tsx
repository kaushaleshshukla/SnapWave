'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function DashboardPage() {
  const { user } = useAuth();
  
  return (
    <div className="container px-4 py-8 mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-600">Welcome back, {user?.full_name || user?.username}!</p>
      </div>
      
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="mb-4 text-xl font-semibold">Account Status</h2>
          <div className="flex items-center mb-4">
            <div className={`w-3 h-3 mr-2 rounded-full ${user?.email_verified ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
            <span>Email: {user?.email_verified ? 'Verified' : 'Not Verified'}</span>
          </div>
          {!user?.email_verified && (
            <button className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
              Resend Verification Email
            </button>
          )}
        </div>
        
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="mb-4 text-xl font-semibold">Profile Completion</h2>
          <div className="w-full h-3 mb-4 bg-gray-200 rounded-full">
            <div 
              className="h-3 bg-green-600 rounded-full" 
              style={{ 
                width: `${calculateProfileCompletion(user)}%` 
              }}
            ></div>
          </div>
          <p className="text-sm text-gray-600">
            Your profile is {calculateProfileCompletion(user)}% complete
          </p>
        </div>
        
        <div className="p-6 bg-white rounded-lg shadow-md">
          <h2 className="mb-4 text-xl font-semibold">Quick Actions</h2>
          <div className="space-y-2">
            <button className="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
              Update Profile
            </button>
            <button className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300">
              Change Password
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function calculateProfileCompletion(user: any) {
  if (!user) return 0;
  
  const fields = [
    !!user.email,
    !!user.username,
    !!user.full_name,
    !!user.bio,
    !!user.profile_picture,
    !!user.email_verified,
  ];
  
  const completedFields = fields.filter(Boolean).length;
  return Math.round((completedFields / fields.length) * 100);
}
