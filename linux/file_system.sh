#!/usr/bin/env bash

# ====================================================================
# base fs operations
touch /tmp/file # create empty file
echo -e "file content\nmore file content" > /tmp/file # create file add write content
cp /tmp/file /tmp/file_copy # copy file
mv /tmp/file_copy /tmp/file2 # move file
rm /tmp/file2 # delete file
mkdir /tmp/folder # create directory
rmdir /tmp/folder # delete directory
rm -rf /tmp/folder # delete directory

# ====================================================================
# read files to stdout
cat /tmp/file
bat -P /tmp/file # https://github.com/sharkdp/bat
tac /tmp/file # read reverse line file to stdout
head /tmp/file # show 10 first lines
tail /tmp/file # show l0 last lines

split README.md /tmp/README_ # split file to files 

# read bytes
hexdump /tmp/file
xxd /tmp/file
hexyl /tmp/file # hex viewer for terminal https://github.com/sharkdp/hexyl


# # ====================================================================
# # file utils
# wc /tmp/file # Print newline, word, and byte counts
# ed # base unix text editor
# tr # Replace(translate) characters
# cut # Cut out fields from `stdin` or files.
# sed # simple text processing

# # file search
# grep # file search
# batgrep # https://github.com/eth-p/bat-extras/blob/master/doc/batgrep.md
# rg # https://github.com/BurntSushi/ripgrep

# # full functional text processing
# awk <pattern> <file>

# shuf
# sort
# uniq

# cmp
# diff
# batdiff # https://github.com/eth-p/bat-extras/blob/master/doc/batdiff.md
# difft # https://github.com/Wilfred/difftastic
# patch

# # ====================================================================
# # file system search
# find
# fd # https://github.com/sharkdp/fd

# # ====================================================================
# # interactive file watcher
# more <file>
# less <file>
# bat <file>
# vi <file>
# nano <file>
# vim <file>
# nvim <file>

# ====================================================================
# file compression
zip /tmp/compressed.zip /tmp/file* # create zip archive (gzip or bzip) 
tar czfv /tmp/compressed.tar.gz /tmp/file* # create tarboll

# ====================================================================
# file links
ln -s /tmp/file /tmp/symbolic # softlink (create new inode) 
ln /tmp/file /tmp/hardlink # hardlink (use same inode)

# # ====================================================================
# rsync /tmp/file /tmp/rsync_file # transefer files

