'use client';

import Link from 'next/link';
import Button from '@/components/ui/Button';

export default function RegistrationSuccessPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="px-8 py-10 mx-auto text-center bg-white shadow-md rounded-xl w-full max-w-md">
        <svg
          className="w-16 h-16 mx-auto mb-4 text-green-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h2 className="mb-4 text-2xl font-bold">Registration Successful!</h2>
        <p className="mb-6 text-gray-600">
          Thank you for registering with SnapWave! We have sent a verification link to your email address.
          Please check your inbox and click the link to verify your account.
        </p>
        <p className="mb-6 text-sm text-gray-500">
          If you don't see the email, please check your spam folder.
        </p>
        <Link href="/login">
          <Button fullWidth>Back to Login</Button>
        </Link>
      </div>
    </div>
  );
}
