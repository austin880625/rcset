# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]; then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi

alias grep='grep --color=auto'

vimscript() {
	vim $1
	chmod +x $1
}
