#!/bin/bash

case $1 in
    build)
        docker build -t banktask -f Dockerfile .
        ;;
    skip_build)
        echo "Skipping the build process..."
        ;;
    *)
esac

case $2 in
  detached)
    docker run -it -d -p 80:80 --name bank_app banktask:latest
    ;;
  current_terminal)
    docker run -it --name bank_app banktask:latest
    ;;
  *)
    echo "Invalid option. Please use 'vscode_detached' to run in your VSCode env by attaching to it or 'current_terminal' to run the bank_app application directly."
    exit 1
    ;;
esac

# docker run -it -d -p 80:80 --name bank_app banktask:latest

# $ docker run -it --name bank_app banktask:latest
# Use this commented out command to just run entrypoint.py by default in your terminal