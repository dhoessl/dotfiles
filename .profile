# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
      . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

if [ -d "/snap/bin" ] ; then
    PATH="/snap/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$HOME/Documents/gitwork" ]; then
    PATH="$HOME/Documents/gitwork:$PATH"
fi

if [ -d "$HOME/gowork" ]; then
  export GOPATH="$HOME/gowork"
  PATH="$PATH:$GOPATH/bin"
fi

if [ -d "/usr/local/go" ]; then
  PATH="$PATH:/usr/local/go/bin"
fi

mdreader () {
  pandoc $1 | lynx -stdin
}

create_role () {
  ROLE_NAME=$1
  mkdir -p roles/$ROLE_NAME/tasks roles/$ROLE_NAME/handlers roles/$ROLE_NAME/templates roles/$ROLE_NAME/files
  echo "---\n..." > roles/$ROLE_NAME/tasks/main.yaml
  echo "---\n..." > roles/$ROLE_NAME/handlers/main.yaml
}

kunde () {
  ssh -t mega kunde
}

mega () {
  ssh -A -t mega zsh
}

export EDITOR='vim'
export VISUAL='vim'

export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh.socket"

[[ -f ~/.bash_aliases ]] && source ~/.bash_aliases
