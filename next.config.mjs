const repositoryName =
  process.env.GITHUB_REPOSITORY?.split("/")[1] ?? "";

const isGitHubActions = process.env.GITHUB_ACTIONS === "true";

const isRootPagesRepository = repositoryName
  .toLowerCase()
  .endsWith(".github.io");

const inferredBasePath =
  isGitHubActions && repositoryName && !isRootPagesRepository
    ? `/${repositoryName}`
    : "";

const configuredBasePath =
  process.env.NEXT_PUBLIC_BASE_PATH ?? inferredBasePath;

const basePath = configuredBasePath.replace(/\/+$/, "");

/** @type {import("next").NextConfig} */
const nextConfig = {
  output: "export",
  trailingSlash: true,
  basePath,

  images: {
    unoptimized: true,
  },

  env: {
    NEXT_PUBLIC_BASE_PATH: basePath,
  },
};

export default nextConfig;
