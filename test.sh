#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTNET_CMD="$(command -v dotnet 2>/dev/null || echo "$HOME/.dotnet/dotnet")"

"$DOTNET_CMD" build "$DIR/Source/MartialArmory/MartialArmory.csproj"
"$DOTNET_CMD" test "$DIR/Source/MartialArmory.Tests/MartialArmory.Tests.csproj" "$@"
