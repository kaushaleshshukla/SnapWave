'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { useAuth } from '@/contexts/AuthContext';
import { userService } from '@/services/api';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

interface ProfileFormData {
  username: string;
  full_name: string;
  bio: string;
}

export default function ProfilePage() {
  const { user, updateProfile } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  
  const { register, handleSubmit, formState: { errors } } = useForm<ProfileFormData>({
    defaultValues: {
      username: user?.username || '',
      full_name: user?.full_name || '',
      bio: user?.bio || '',
    }
  });
  
  const onSubmit = async (data: ProfileFormData) => {
    setIsLoading(true);
    try {
      await updateProfile(data);
      toast.success('Profile updated successfully!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleProfilePictureUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Check file type
    if (!file.type.includes('image/')) {
      toast.error('Please upload an image file');
      return;
    }
    
    // Check file size (limit to 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('Image size should be less than 5MB');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    setUploading(true);
    try {
      await userService.uploadProfilePicture(formData);
      // Update user context with new profile picture
      const userData = await userService.getProfile();
      updateProfile(userData);
      toast.success('Profile picture updated!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to upload profile picture.');
    } finally {
      setUploading(false);
    }
  };
  
  return (
    <div className="container px-4 py-8 mx-auto max-w-2xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Your Profile</h1>
        <p className="text-gray-600">Update your personal information</p>
      </div>
      
      <div className="p-6 mb-8 bg-white rounded-lg shadow-md">
        <div className="flex flex-col items-center mb-8 sm:flex-row sm:items-start">
          <div className="relative mb-4 sm:mb-0 sm:mr-8">
            <div className="w-24 h-24 overflow-hidden bg-gray-200 rounded-full">
              {user?.profile_picture ? (
                <img
                  src={user.profile_picture}
                  alt="Profile"
                  className="object-cover w-full h-full"
                />
              ) : (
                <div className="flex items-center justify-center w-full h-full text-3xl font-semibold text-gray-400">
                  {user?.username?.charAt(0).toUpperCase() || '?'}
                </div>
              )}
            </div>
            
            <label
              htmlFor="profile-picture"
              className="absolute bottom-0 right-0 flex items-center justify-center w-8 h-8 bg-white rounded-full cursor-pointer shadow-md"
            >
              <svg
                className="w-4 h-4 text-gray-700"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                />
              </svg>
              <input
                id="profile-picture"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleProfilePictureUpload}
                disabled={uploading}
              />
            </label>
            
            {uploading && (
              <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-full">
                <div className="w-6 h-6 border-t-2 border-b-2 border-blue-500 rounded-full animate-spin"></div>
              </div>
            )}
          </div>
          
          <div className="text-center sm:text-left">
            <h2 className="text-xl font-semibold">{user?.full_name || user?.username}</h2>
            <p className="text-gray-500">@{user?.username}</p>
            <div className="mt-2">
              <span className={`px-2 py-1 text-xs font-medium rounded ${
                user?.email_verified
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {user?.email_verified ? 'Verified' : 'Unverified'}
              </span>
            </div>
          </div>
        </div>
        
        <form onSubmit={handleSubmit(onSubmit)}>
          <Input
            id="username"
            type="text"
            label="Username"
            placeholder="Your username"
            fullWidth
            {...register('username', {
              required: 'Username is required',
              minLength: {
                value: 3,
                message: 'Username must be at least 3 characters'
              },
              maxLength: {
                value: 20,
                message: 'Username must be at most 20 characters'
              },
              pattern: {
                value: /^[a-zA-Z0-9_]+$/,
                message: 'Username can only contain letters, numbers, and underscores'
              }
            })}
            error={errors.username?.message}
          />
          
          <Input
            id="full_name"
            type="text"
            label="Full Name"
            placeholder="Your full name"
            fullWidth
            {...register('full_name')}
            error={errors.full_name?.message}
          />
          
          <div className="mb-4">
            <label htmlFor="bio" className="block mb-2 text-sm font-medium text-gray-700">
              Bio
            </label>
            <textarea
              id="bio"
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Write something about yourself..."
              {...register('bio')}
            ></textarea>
            {errors.bio && <p className="mt-1 text-sm text-red-600">{errors.bio.message}</p>}
          </div>
          
          <div className="flex justify-end">
            <Button type="submit" isLoading={isLoading}>
              Save Changes
            </Button>
          </div>
        </form>
      </div>
      
      <div className="p-6 bg-white rounded-lg shadow-md">
        <h2 className="mb-4 text-xl font-semibold">Account Information</h2>
        <div className="mb-4">
          <label className="block mb-1 text-sm font-medium text-gray-700">Email Address</label>
          <div className="flex items-center">
            <p className="text-gray-900">{user?.email}</p>
            {!user?.email_verified && (
              <button className="ml-4 text-sm font-medium text-blue-600 hover:text-blue-500">
                Verify
              </button>
            )}
          </div>
        </div>
        
        <div className="pt-4 mt-4 border-t border-gray-200">
          <h3 className="mb-4 text-lg font-medium">Security</h3>
          <Button variant="outline">
            Change Password
          </Button>
        </div>
      </div>
    </div>
  );
}
