#!/bin/zsh
set -eu

usage() {
  cat <<'USAGE'
Usage:
  restart-macos-app-via-launchd.sh --app <AppName> [--delay seconds] [--dry-run] [--cleanup-files]

Examples:
  restart-macos-app-via-launchd.sh --app Codex --delay 8 --dry-run
  restart-macos-app-via-launchd.sh --app Codex --delay 8

Notes:
  - Uses launchd so the restart continues after the current agent app exits.
  - Falls back to terminating only processes under the resolved app bundle.
  - Writes one-shot worker/log files to /private/tmp.
USAGE
}

APP_NAME=""
DELAY_SECONDS="8"
DRY_RUN="false"
CLEANUP_FILES="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --app)
      APP_NAME="${2:-}"
      shift 2
      ;;
    --delay)
      DELAY_SECONDS="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    --cleanup-files)
      CLEANUP_FILES="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "${APP_NAME}" ]]; then
  echo "--app is required" >&2
  usage >&2
  exit 2
fi

if ! [[ "${DELAY_SECONDS}" == <-> ]]; then
  echo "--delay must be a non-negative integer" >&2
  exit 2
fi

APP_PATH="$(/usr/bin/osascript -e "POSIX path of (path to application \"${APP_NAME}\")" 2>/dev/null || true)"
APP_CONTENTS=""
if [[ -n "${APP_PATH}" && -d "${APP_PATH%/}/Contents" ]]; then
  APP_CONTENTS="${APP_PATH%/}/Contents"
fi

SLUG="$(echo "${APP_NAME}" | /usr/bin/tr '[:upper:]' '[:lower:]' | /usr/bin/tr -cs 'a-z0-9' '-' | /usr/bin/sed 's/^-//;s/-$//')"
if [[ -z "${SLUG}" ]]; then
  SLUG="app"
fi

RUN_ID="$(/bin/date +%s)"
LABEL="com.${USER}.macos-app-external-restart.${SLUG}.${RUN_ID}"
BASE="/private/tmp/${LABEL}"
WORKER="${BASE}.worker.zsh"
LOG_FILE="${BASE}.log"
RUNNER_LOG="${BASE}.runner.log"
LABEL_FILE="${BASE}.label"

echo "label=${LABEL}"
echo "worker=${WORKER}"
echo "log=${LOG_FILE}"
echo "runner_log=${RUNNER_LOG}"
if [[ -n "${APP_CONTENTS}" ]]; then
  echo "bundle_contents=${APP_CONTENTS}"
else
  echo "bundle_contents="
  echo "warning=could not resolve app bundle; graceful quit/open can still run, fallback termination will be skipped" >&2
fi

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "dry_run=true"
  exit 0
fi

/bin/cat > "${WORKER}" <<'WORKER'
#!/bin/zsh
set -u

APP_NAME="$1"
DELAY_SECONDS="$2"
APP_CONTENTS="$3"
LOG_FILE="$4"
CLEANUP_FILES="$5"
WORKER_PATH="$6"
LABEL_FILE="$7"
RUNNER_LOG="$8"

{
  echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] scheduled restart for ${APP_NAME} after ${DELAY_SECONDS}s"
  /bin/sleep "${DELAY_SECONDS}"

  echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] requesting graceful ${APP_NAME} quit"
  /usr/bin/osascript -e "tell application \"${APP_NAME}\" to quit" || true

  for _ in {1..12}; do
    running="$(/usr/bin/osascript -e "application \"${APP_NAME}\" is running" 2>/dev/null || echo false)"
    if [[ "${running}" != "true" ]]; then
      break
    fi
    /bin/sleep 1
  done

  running="$(/usr/bin/osascript -e "application \"${APP_NAME}\" is running" 2>/dev/null || echo false)"
  if [[ "${running}" == "true" ]]; then
    if [[ -n "${APP_CONTENTS}" && -d "${APP_CONTENTS}" ]]; then
      echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] ${APP_NAME} still running; terminating bundle processes under ${APP_CONTENTS}"
      /usr/bin/pkill -TERM -f "${APP_CONTENTS}" || true
    else
      echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] ${APP_NAME} still running; no bundle path resolved, skipping fallback termination"
    fi
    /bin/sleep 3
  fi

  echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] opening ${APP_NAME}"
  /usr/bin/open -a "${APP_NAME}"
  /bin/sleep 5

  running="$(/usr/bin/osascript -e "application \"${APP_NAME}\" is running" 2>/dev/null || echo false)"
  echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] ${APP_NAME} running: ${running}"

  if [[ "${XPC_SERVICE_NAME:-}" == com.*.macos-app-external-restart.* ]]; then
    echo "[$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ')] removing launchd job ${XPC_SERVICE_NAME}"
    /bin/launchctl remove "${XPC_SERVICE_NAME}" || true
  fi
} >> "${LOG_FILE}" 2>&1

if [[ "${CLEANUP_FILES}" == "true" ]]; then
  /bin/sleep 2
  /bin/rm -f "${WORKER_PATH}" "${LABEL_FILE}" "${RUNNER_LOG}" "${LOG_FILE}"
fi
WORKER

/bin/chmod +x "${WORKER}"
echo "${LABEL}" > "${LABEL_FILE}"

/bin/launchctl submit -l "${LABEL}" -o "${RUNNER_LOG}" -e "${RUNNER_LOG}" -- \
  "${WORKER}" "${APP_NAME}" "${DELAY_SECONDS}" "${APP_CONTENTS}" "${LOG_FILE}" \
  "${CLEANUP_FILES}" "${WORKER}" "${LABEL_FILE}" "${RUNNER_LOG}"

echo "submitted=${LABEL}"
echo "verify_log=${LOG_FILE}"
