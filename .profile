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
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
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

SSH_ENV="$HOME/.ssh/env"

start_ssh_agent () {
  ps -ef | grep ${SSH_AGENT_PID} | grep -v grep > /dev/null && killall ssh-agent
  /usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
  chmod 600 "${SSH_ENV}"
  . "${SSH_ENV}" > /dev/null
  /usr/bin/ssh-add;
}

if [ -f "${SSH_ENV}" ]; then
  . "${SSH_ENV}" > /dev/null
  ps -ef | grep ${SSH_AGENT_PID} | grep -v grep > /dev/null || { start_ssh_agent; }
else
  start_ssh_agent;
fi

export EDITOR='vim'
export VISUAL='vim'

[[ -f ~/.bash_aliases ]] && source ~/.bash_aliases
