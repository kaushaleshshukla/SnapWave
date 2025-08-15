'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { toast } from 'react-toastify';
import { authService } from '@/services/api';
import Button from '@/components/ui/Button';

export default function VerifyEmailPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const searchParams = useSearchParams();
  
  useEffect(() => {
    const verifyEmail = async () => {
      const token = searchParams.get('token');
      if (!token) {
        setError('Invalid or missing verification token');
        setIsLoading(false);
        return;
      }
      
      try {
        await authService.verifyEmail(token);
        setIsSuccess(true);
        toast.success('Email verified successfully!');
      } catch (error: any) {
        setError(error.response?.data?.detail || 'Failed to verify email. The link may have expired.');
        toast.error('Email verification failed');
      } finally {
        setIsLoading(false);
      }
    };
    
    verifyEmail();
  }, [searchParams, router]);
  
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="px-8 py-10 mx-auto text-center bg-white shadow-md rounded-xl w-full max-w-md">
        {isLoading ? (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 border-t-2 border-b-2 border-blue-500 rounded-full animate-spin"></div>
            <p className="mt-4 text-xl">Verifying your email...</p>
          </div>
        ) : isSuccess ? (
          <>
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
            <h2 className="mb-4 text-2xl font-bold">Email Verified</h2>
            <p className="mb-6 text-gray-600">
              Your email has been successfully verified. You can now access all features of your account.
            </p>
            <Link href="/login">
              <Button fullWidth>Go to Login</Button>
            </Link>
          </>
        ) : (
          <>
            <svg
              className="w-16 h-16 mx-auto mb-4 text-red-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h2 className="mb-4 text-2xl font-bold">Verification Failed</h2>
            <p className="mb-6 text-gray-600">{error}</p>
            <Link href="/login">
              <Button fullWidth variant="outline">
                Back to Login
              </Button>
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
