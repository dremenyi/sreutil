#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please install it and try again."
    exit 1
fi

# Determine the OS and set the virtual environment path
case "$(uname -s)" in
    Darwin)
        # macOS
        VENV_PATH="$HOME/.cfaws_venv"
        if [ "$SHELL" = "/bin/zsh" ]; then
            SHELL_PROFILE="$HOME/.zshrc"
        elif [ "$SHELL" = "/usr/local/bin/fish" ]; then
            SHELL_PROFILE="$HOME/.config/fish/config.fish"
        elif [ "$TERM_PROGRAM" = "iTerm.app" ] || [ "$TERM_PROGRAM" = "iTerm2.app" ]; then
            if [ -f "$HOME/.iterm2_shell_integration.zsh" ]; then
                SHELL_PROFILE="$HOME/.iterm2_shell_integration.zsh"
            elif [ -f "$HOME/.iterm2_shell_integration.fish" ]; then
                SHELL_PROFILE="$HOME/.iterm2_shell_integration.fish"
            else
                SHELL_PROFILE="$HOME/.zshrc"
            fi
        else
            SHELL_PROFILE="$HOME/.bash_profile"
        fi
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        # Windows
        VENV_PATH="$USERPROFILE\\.cfaws_venv"
        SHELL_PROFILE="$USERPROFILE\\.bash_profile"  # Adjust as needed
        ;;
    *)
        echo "Unsupported OS. This script only supports macOS and Windows."
        exit 1
        ;;
esac

# Create a virtual environment
python3 -m venv "$VENV_PATH"

# Activate the virtual environment
if [ "$(uname -s)" = "Darwin" ]; then
    source "$VENV_PATH/bin/activate"
else
    source "$VENV_PATH/Scripts/activate"
fi

# Upgrade pip
pip install --upgrade pip

# Navigate to the project root directory
cd "$(dirname "$0")"

# Install the module in editable mode
pip install --editable .

# Add CFAWS to PATH in the shell profile if not already added
if ! grep -q "$VENV_PATH/bin" "$SHELL_PROFILE"; then
    if [ "$SHELL" = "/usr/local/bin/fish" ]; then
        echo "set -gx PATH \"$VENV_PATH/bin\" \$PATH" >> "$SHELL_PROFILE"
    else
        echo "export PATH=\"$VENV_PATH/bin:\$PATH\"" >> "$SHELL_PROFILE"
    fi
    echo "Added $VENV_PATH/bin to PATH in $SHELL_PROFILE"
else
    echo "$VENV_PATH/bin is already in PATH in $SHELL_PROFILE"
fi

# Source the shell profile to apply changes immediately
source "$SHELL_PROFILE"

# Deactivate the virtual environment
deactivate

echo "Setup complete. The virtual environment is installed at $VENV_PATH. The PATH has been updated in $SHELL_PROFILE."
echo "To activate the virtual environment manually, run 'source $VENV_PATH/bin/activate' on macOS or '$VENV_PATH\\Scripts\\activate' on Windows."
