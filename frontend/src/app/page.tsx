import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container px-4 mx-auto">
        {/* Hero Section */}
        <div className="py-20 md:py-32 text-center">
          <h1 className="mb-6 text-4xl font-bold tracking-tight text-gray-900 md:text-6xl">
            Share your special moments with SnapWave
          </h1>
          <p className="max-w-2xl mx-auto mb-10 text-xl text-gray-600">
            Connect with friends, share your life&apos;s best moments, and explore content from people around the world.
          </p>
          
          <div className="flex flex-col items-center justify-center space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
            <Link
              href="/register" 
              className="px-8 py-3 text-lg font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="px-8 py-3 text-lg font-medium text-blue-700 bg-blue-100 rounded-md hover:bg-blue-200"
            >
              Sign In
            </Link>
          </div>
        </div>
        
        {/* Features Section */}
        <div className="py-16">
          <h2 className="mb-12 text-3xl font-bold text-center">Why choose SnapWave?</h2>
          
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="flex items-center justify-center w-12 h-12 mb-4 bg-blue-100 rounded-full">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-semibold">Share Photos</h3>
              <p className="text-gray-600">Upload and share your favorite moments with friends and followers.</p>
            </div>
            
            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="flex items-center justify-center w-12 h-12 mb-4 bg-blue-100 rounded-full">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-semibold">Connect with Friends</h3>
              <p className="text-gray-600">Find and connect with friends, family, and interesting people.</p>
            </div>
            
            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="flex items-center justify-center w-12 h-12 mb-4 bg-blue-100 rounded-full">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-semibold">Private & Secure</h3>
              <p className="text-gray-600">Your data is secure with advanced encryption and privacy controls.</p>
            </div>
          </div>
        </div>
        
        {/* CTA Section */}
        <div className="py-16 text-center">
          <h2 className="mb-6 text-3xl font-bold">Ready to join SnapWave?</h2>
          <p className="max-w-2xl mx-auto mb-8 text-xl text-gray-600">
            Create an account today and start sharing your moments with the world.
          </p>
          <Link
            href="/register"
            className="px-8 py-3 text-lg font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Sign Up Now
          </Link>
        </div>
      </div>
    </div>
  );
}
