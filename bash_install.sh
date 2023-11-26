#!/bin/bash

SH_START_MARKER="###RCSET_START###"
SH_END_MARKER="###RCSET_END###"

process_bashrc() {
	if [ ! -f "~/.bashrc" ]; then
		touch ~/.bashrc
	fi
	cat ~/.bashrc | awk 'BEGIN{start=0}
	/^###RCSET_START###$/ {start=1;}
	{if (start != 1) print $0;}
	/^###RCSET_END###$/ {start=0;}
	' > bashrc.new
	echo "###RCSET_START###" >> bashrc.new
	cat bashrc >> bashrc.new
	cat hiscript/bashrc >> bashrc.new
	cp hiscript/hiscript.py ~/.local/bin/hiscript.py
	cat cdd/bashrc >> bashrc.new
	echo "###RCSET_END###" >> bashrc.new

	cp bashrc.new ~/.bashrc
	rm bashrc.new
}

process_vimrc() {
	if [ ! -f "~/.vimrc" ]; then
		touch ~/.vimrc
	fi
	mkdir -p $HOME/.vim/swapfiles
	cat ~/.vimrc | awk 'BEGIN{start=0}
	/^"##RCSET_START###$/ {start=1;}
	{if (start != 1) print $0;}
	/^"##RCSET_END###$/ {start=0;}
	' > vimrc.new
	echo '"##RCSET_START###' >> vimrc.new
	cat vimrc >> vimrc.new
	echo '"##RCSET_END###' >> vimrc.new

	cp vimrc.new ~/.vimrc
	rm bashrc.new
}

process_bashrc
process_vimrc

unset SH_START_MARKER
unset SH_END_MARKER
