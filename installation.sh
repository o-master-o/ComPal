#!/bin/bash

SCRIPT_DIR=$(realpath $(dirname "$0"))
REQUIREMENTS_DIR_PATH="$SCRIPT_DIR/requirements/basic.txt"
BASHRC="$HOME/.bashrc"
VENV_DIR=$SCRIPT_DIR/venv
VENV_PYTHON_PATH="$VENV_DIR/bin/python"
CONFIG_DIR_PATH="$HOME/.config/com_pal"

VOCAB_LINK="https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/vocab.bpe"
ENCODER_LINK="https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/encoder.json"
GPT_MODEL_LINK="https://gpt4all.io/models/gguf/gpt4all-falcon-newbpe-q4_0.gguf"
# WHISPER_MODEL_LINK="https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt"
WHISPER_MODEL_LINK="https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt"

# Colors
BLUE="\033[34;1m"
NC="\033[0m"

clear_screen () {
    clear -x
}

remove_venv () {
    rm -rf "$SCRIPT_DIR/venv"
}

remove_tmp() {
    rm -rf "$CONFIG_DIR_PATH"
}

clean_environment () {
    remove_venv
    remove_tmp
}

create_virtualenv() {
    local python_executable=${1:-python}
    echo "hello $python_executable"
    virtualenv -p $python_executable "$VENV_DIR"
    echo "Virtual environment created in $VENV_DIR"
}

install_requirements() {
    pip install -r "$1"
}

install_if_not_installed() {
    package=$1

    if ! dpkg -s "$package" &> /dev/null; then
        echo "Package $package is not installed. Installing..."
        sudo apt-get update
        sudo apt-get install -y "$package"
    else
        echo "Package $package is already installed."
    fi
}

get_resources() {
#     mkdir -p "$CONFIG_DIR_PATH"
#     curl -o "$CONFIG_DIR_PATH/vocab.bpe" "$VOCAB_LINK"
#     curl -o "$CONFIG_DIR_PATH/encoder.json" "$ENCODER_LINK"
#     curl -o "$CONFIG_DIR_PATH/gpt4all-falcon-newbpe-q4_0.gguf" "$GPT_MODEL_LINK"
    curl -o "$CONFIG_DIR_PATH/tiny.pt" "$WHISPER_MODEL_LINK"
}

# Installation steps ---------->
clear_screen
echo -e "${BLUE}Installation start${NC}"
clean_environment
install_if_not_installed virtualenv
install_if_not_installed portaudio19-dev
install_if_not_installed libespeak-dev
install_if_not_installed pulseaudio
install_if_not_installed libpulse-dev
install_if_not_installed osspd
create_virtualenv "$1"

source "$VENV_DIR/bin/activate"
install_requirements "$REQUIREMENTS_DIR_PATH"
deactivate

get_resources

clear_screen
echo -e "${BLUE}Installation complete${NC}"
