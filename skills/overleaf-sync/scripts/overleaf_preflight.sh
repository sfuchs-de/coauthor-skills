#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  printf 'usage: %s <clone-path> [remote-branch]\n' "$0" >&2
  exit 2
fi

clone=$1
branch=${2:-}

git -C "$clone" rev-parse --is-inside-work-tree >/dev/null

if [[ -z "$branch" ]]; then
  branch=$(git -C "$clone" config --get "branch.$(git -C "$clone" branch --show-current).merge" 2>/dev/null || true)
  branch=${branch#refs/heads/}
fi
if [[ -z "$branch" ]]; then
  branch=$(git -C "$clone" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)
  branch=${branch#origin/}
fi
if [[ -z "$branch" ]]; then
  branch=main
fi

remote_url=$(git -C "$clone" config --get remote.origin.url || true)
if [[ "$remote_url" != *git.overleaf.com* ]]; then
  printf 'error: origin is not an Overleaf Git remote\n' >&2
  exit 3
fi

git -C "$clone" fetch --quiet origin "$branch"

head=$(git -C "$clone" rev-parse HEAD)
remote=$(git -C "$clone" rev-parse FETCH_HEAD)
read -r ahead behind < <(git -C "$clone" rev-list --left-right --count HEAD...FETCH_HEAD)

tracked=$(git -C "$clone" status --porcelain --untracked-files=no | wc -l | tr -d ' ')
untracked=$(git -C "$clone" status --porcelain | awk 'substr($0,1,2)=="??" {n++} END {print n+0}')

printf 'clone=%s\n' "$clone"
printf 'branch=%s\n' "$branch"
printf 'head=%s\n' "$head"
printf 'remote_head=%s\n' "$remote"
printf 'ahead=%s\n' "$ahead"
printf 'behind=%s\n' "$behind"
printf 'tracked_changes=%s\n' "$tracked"
printf 'untracked_paths=%s\n' "$untracked"
