'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { authService } from '@/services/api';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

interface ForgotPasswordFormData {
  email: string;
}

export default function ForgotPasswordPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  
  const { register, handleSubmit, formState: { errors } } = useForm<ForgotPasswordFormData>();
  
  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsLoading(true);
    try {
      await authService.requestPasswordReset(data.email);
      setIsSubmitted(true);
      toast.success('Password reset instructions sent to your email.');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to request password reset.');
    } finally {
      setIsLoading(false);
    }
  };
  
  if (isSubmitted) {
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
          <h2 className="mb-4 text-2xl font-bold">Check your email</h2>
          <p className="mb-6 text-gray-600">
            We have sent password recovery instructions to your email.
            Please check your inbox and follow the instructions.
          </p>
          <Link
            href="/login"
            className="inline-block w-full py-2 font-medium text-center text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Return to login
          </Link>
        </div>
      </div>
    );
  }
  
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="px-8 py-10 mx-auto bg-white shadow-md rounded-xl w-full max-w-md">
        <div className="mb-10 text-center">
          <h1 className="mb-2 text-3xl font-bold">Reset Password</h1>
          <p className="text-gray-600">Enter your email to receive reset instructions</p>
        </div>
        
        <form onSubmit={handleSubmit(onSubmit)}>
          <Input
            id="email"
            type="email"
            label="Email Address"
            placeholder="Enter your email"
            fullWidth
            {...register('email', { 
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email address'
              }
            })}
            error={errors.email?.message}
          />
          
          <div className="mt-6">
            <Button type="submit" fullWidth isLoading={isLoading}>
              Send Reset Instructions
            </Button>
          </div>
        </form>
        
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Remembered your password?{' '}
            <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
              Back to login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
