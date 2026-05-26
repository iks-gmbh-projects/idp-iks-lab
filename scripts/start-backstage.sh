#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${IKS_BACKSTAGE_APP_NAME:-iks-idp}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE_DIR="$(cd "${REPO_ROOT}/.." && pwd)"
DEFAULT_RUNTIME_DIR="${WORKSPACE_DIR}/iks-backstage-runtime"
CACHE_BASE="${XDG_CACHE_HOME:-${HOME:-/tmp}/.cache}"
CACHE_RUNTIME_DIR="${CACHE_BASE}/idp-iks-lab/iks-backstage-runtime"
SOURCE_CONFIG="${REPO_ROOT}/backstage/app-config.local.example.yaml"
CATALOG_TARGET="${REPO_ROOT}/backstage/catalog/locations.yaml"

resolve_runtime_dir() {
  if [ -n "${IKS_BACKSTAGE_RUNTIME_DIR:-}" ]; then
    case "${IKS_BACKSTAGE_RUNTIME_DIR}" in
      /*) printf '%s\n' "${IKS_BACKSTAGE_RUNTIME_DIR}" ;;
      *) printf '%s/%s\n' "${REPO_ROOT}" "${IKS_BACKSTAGE_RUNTIME_DIR}" ;;
    esac
    return
  fi

  if [ -d "${DEFAULT_RUNTIME_DIR}" ] || [ -w "${WORKSPACE_DIR}" ]; then
    printf '%s\n' "${DEFAULT_RUNTIME_DIR}"
    return
  fi

  printf '%s\n' "${CACHE_RUNTIME_DIR}"
}

RUNTIME_DIR="$(resolve_runtime_dir)"
RUNTIME_PARENT="$(dirname "${RUNTIME_DIR}")"
RUNTIME_NAME="$(basename "${RUNTIME_DIR}")"
LOCAL_CONFIG="${RUNTIME_DIR}/app-config.local.yaml"

echo "IKS IDP Backstage local runtime"
echo "Repository: ${REPO_ROOT}"
echo "Runtime:    ${RUNTIME_DIR}"

if [ "${RUNTIME_DIR}" != "${DEFAULT_RUNTIME_DIR}" ] && [ -z "${IKS_BACKSTAGE_RUNTIME_DIR:-}" ]; then
  echo "Note: ${WORKSPACE_DIR} is not writable, using cache runtime instead."
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx is required to create the local Backstage runtime." >&2
  exit 1
fi

if ! command -v yarn >/dev/null 2>&1; then
  echo "Error: yarn is required to start the generated Backstage app." >&2
  exit 1
fi

mkdir -p "${RUNTIME_PARENT}"
if [ ! -w "${RUNTIME_PARENT}" ]; then
  echo "Error: runtime parent is not writable: ${RUNTIME_PARENT}" >&2
  echo "Set IKS_BACKSTAGE_RUNTIME_DIR to a writable directory and run again." >&2
  exit 1
fi

if [ ! -d "${RUNTIME_DIR}" ]; then
  echo
  echo "Creating local Backstage runtime in ${RUNTIME_DIR}"
  echo "This first run downloads dependencies and can take several minutes."
  (
    cd "${RUNTIME_PARENT}"
    printf '%s\n' "${APP_NAME}" | npx --yes @backstage/create-app@latest --path "${RUNTIME_NAME}"
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
  catalog_target_for_sed="${CATALOG_TARGET//&/\&}"
  sed "s|target: ../idp-iks-lab/backstage/catalog/locations.yaml|target: ${catalog_target_for_sed}|" \
    "${SOURCE_CONFIG}" > "${LOCAL_CONFIG}"
fi

echo
echo "Starting Backstage..."
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:7007"
echo

cd "${RUNTIME_DIR}"
exec yarn dev
