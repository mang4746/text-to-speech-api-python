#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$ROOT_DIR"

# Obtener la versión desde el archivo VERSION
VERSION=$(tr -d '[:space:]' < VERSION)

if [[ -z "$VERSION" ]]; then
  echo "El archivo VERSION está vacío."
  exit 1
fi

# Detectar sistema operativo y arquitectura
OS=$(uname -s)
ARCH=$(uname -m)

echo "----------------------"
echo "Sistema operativo: $OS"
echo "Arquitectura: $ARCH"
echo "Versión del proyecto: $VERSION"
echo "----------------------"

# echo "----------------------"
# echo "Pull code desde TFS"
# echo "----------------------"
# git pull origin HEAD

LOCAL_IMAGE="text-to-speech-api"
REGISTRY_IMAGE="bdpsam443/text-to-speech-api"
VERSION_IMAGE="$LOCAL_IMAGE:$VERSION"
LATEST_IMAGE="$LOCAL_IMAGE:latest"

echo "Construyendo imagen $VERSION_IMAGE..."

# En macOS ARM se carga localmente una imagen Linux amd64 para que Compose
# pueda utilizarla sin descargarla del registro.
if [[ "$OS" == "Darwin" && "$ARCH" == "arm64" ]]; then
  docker buildx build \
    --platform linux/amd64 \
    -t "$VERSION_IMAGE" \
    -t "$LATEST_IMAGE" \
    --load .
else
  docker build \
    -t "$VERSION_IMAGE" \
    -t "$LATEST_IMAGE" .
fi

# Publicar la imagen en el registro si se ha configurado la variable PUSH_IMAGE
if [[ "${PUSH_IMAGE:-false}" == "true" ]]; then
  REGISTRY_VERSION_IMAGE="$REGISTRY_IMAGE:$VERSION"
  REGISTRY_LATEST_IMAGE="$REGISTRY_IMAGE:latest"

  echo "Publicando $REGISTRY_VERSION_IMAGE..."
  docker tag "$VERSION_IMAGE" "$REGISTRY_VERSION_IMAGE"
  docker push "$REGISTRY_VERSION_IMAGE"

  echo "Publicando $REGISTRY_LATEST_IMAGE..."
  docker tag "$LATEST_IMAGE" "$REGISTRY_LATEST_IMAGE"
  docker push "$REGISTRY_LATEST_IMAGE"
fi

echo "Imagen local preparada: $VERSION_IMAGE"

