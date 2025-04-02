/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:80/:path*' // Proxy API requests to FastAPI backend
      }
    ];
  }
};

export default nextConfig;
