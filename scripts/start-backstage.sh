#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE_DIR="$(cd "${REPO_ROOT}/.." && pwd)"
RUNTIME_DIR="${WORKSPACE_DIR}/iks-backstage-runtime"
LOCAL_CONFIG="${RUNTIME_DIR}/app-config.local.yaml"
SOURCE_CONFIG="${REPO_ROOT}/backstage/app-config.local.example.yaml"

echo "IKS IDP Backstage local runtime"
echo "Repository: ${REPO_ROOT}"
echo "Runtime:    ${RUNTIME_DIR}"

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx is required to create the local Backstage runtime." >&2
  exit 1
fi

if ! command -v yarn >/dev/null 2>&1; then
  echo "Error: yarn is required to start the generated Backstage app." >&2
  exit 1
fi

if [ ! -d "${RUNTIME_DIR}" ]; then
  echo
  echo "Creating local Backstage runtime in ${RUNTIME_DIR}"
  echo "This first run downloads dependencies and can take several minutes."
  (
    cd "${WORKSPACE_DIR}"
    npx @backstage/create-app@latest --path iks-backstage-runtime
  )
fi

if [ ! -f "${RUNTIME_DIR}/package.json" ]; then
  echo "Error: ${RUNTIME_DIR} exists but does not look like a generated Backstage app." >&2
  echo "Remove or rename it, then run this script again to bootstrap a fresh runtime." >&2
  exit 1
fi

if [ ! -f "${LOCAL_CONFIG}" ]; then
  echo
  echo "Creating local runtime config: ${LOCAL_CONFIG}"
  cp "${SOURCE_CONFIG}" "${LOCAL_CONFIG}"
fi

echo
echo "Starting Backstage..."
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:7007"
echo

cd "${RUNTIME_DIR}"
exec yarn dev
