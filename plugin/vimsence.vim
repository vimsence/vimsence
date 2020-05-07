if !has('python3')
    echo 'vim has to be compiled with +python3 to run vimsence'
    finish
endif

if exists('g:vimsence_loaded')
    finish
endif

if !exists('g:vimsence_discord_flatpak')
    " Flatpak support is disabled by default.
    " This has no effect on Windows.
    let g:vimsence_discord_flatpak=0
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

import vimsence
EOF

function! DiscordUpdatePresence()
    python3 vimsence.update_presence()
endfunction

function! DiscordReconnect()
    python3 vimsence.reconnect()
endfunction

function! DiscordDisconnect()
    python3 vimsence.disconnect()
endfunction

command! -nargs=0 UpdatePresence echo "This command has been deprecated. Use :DiscordUpdatePresence instead."
command! -nargs=0 DiscordUpdatePresence call DiscordUpdatePresence()
command! -nargs=0 DiscordReconnect call DiscordReconnect()
command! -nargs=0 DiscordDisconnect call DiscordDisconnect()

augroup DiscordPresence
    autocmd!
    autocmd BufNewFile,BufRead,BufEnter * :call DiscordUpdatePresence()
augroup END

let g:vimsence_loaded = 1
