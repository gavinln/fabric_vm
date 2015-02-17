#!/bin/bash

if [ ! -d ~/.oh-my-zsh ]; then
    wget --no-check-certificate http://install.ohmyz.sh -O - | sh
    chsh -s /bin/zsh
fi

echo Adding fabric to plugins list in vim ~/.zshrc
sed -i 's/^plugins=.*/plugins=(git fabric)/' ~/.zshrc

# get z (fast cd) script and install if not already setup
ZSH_z="source ~/z.sh"
wget -O ~/z.sh https://raw.githubusercontent.com/rupa/z/master/z.sh
grep -q -F "$ZSH_z" ~/.zshrc || echo $ZSH_z >> ~/.zshrc
