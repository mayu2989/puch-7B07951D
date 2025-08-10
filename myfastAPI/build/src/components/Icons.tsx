import React from 'react';

// Icons are now in a '.tsx' file for TypeScript consistency.
// The code itself is pure JSX and doesn't require any changes.

export const FileUpIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M15 22v-4a4.8 4.8 0 0 0-3-4v-2" />
    <path d="M9 12v2a4.8 4.8 0 0 0 3 4v4" />
    <path d="M12 2v-2" />
    <path d="M12 24v-2" />
    <path d="M22 12h-2" />
    <path d="M2 12h2" />
    <path d="M19.4 4.6l-1.4 1.4" />
    <path d="M6.6 19.4l1.4-1.4" />
    <path d="M4.6 19.4l1.4-1.4" />
    <path d="M19.4 4.6l-1.4 1.4" />
    <path d="m5 5 5 5" />
    <path d="m14 14 5 5" />
  </svg>
);

export const MusicIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M2 17v-3a4 4 0 0 1 4-4 4 4 0 0 1 4 4v3" />
    <path d="M18 17v-3a4 4 0 0 1 4-4 4 4 0 0 1 4 4v3" />
    <path d="M8 12V3a4 4 0 0 1 4 4 4 4 0 0 1 4-4v9" />
    <path d="M2 22h20" />
  </svg>
);

export const Loader2Icon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
  </svg>
);

export const ErrorIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M18 6L6 18" />
    <path d="M6 6l12 12" />
  </svg>
);
