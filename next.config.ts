/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  // Add your repository name between the slashes below:
  basePath: '/my-repository-name', 
};

module.exports = nextConfig;
