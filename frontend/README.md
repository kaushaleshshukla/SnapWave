# SnapWave Frontend

This is the frontend application for SnapWave, a social media platform for sharing your special moments with friends and the world.

## Features

- User authentication (login, register, email verification)
- Password reset functionality
- User profile management
- Dashboard with user statistics
- Responsive design for all devices

## Tech Stack

- Next.js 14
- React
- TypeScript
- Tailwind CSS
- Axios for API requests
- React Hook Form for form handling
- React Toastify for notifications

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- npm or yarn
- Backend API running (see backend README)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/SnapWave.git
cd SnapWave/frontend
```

2. Install dependencies
```bash
npm install
```

3. Configure environment variables
Create a `.env.local` file in the root directory with the following:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

4. Run the development server
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

- `src/app` - App router pages and layouts
- `src/components` - Reusable UI components
- `src/contexts` - React context providers
- `src/services` - API service functions
- `public` - Static assets

## Authentication Flow

1. User registers with email, username, and password
2. Backend sends verification email
3. User confirms email by clicking link
4. User can now log in with email and password
5. JWT token is stored in local storage for authenticated requests
