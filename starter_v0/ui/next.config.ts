import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: [
    'sim-source-hash-arms.trycloudflare.com',
    '*.trycloudflare.com'
  ],
};

export default nextConfig;
