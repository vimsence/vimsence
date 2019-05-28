if !has('python3')
    echo 'vim has to be compiled with +python3 to run vimsence'
    finish
endif

if exists('g:vimsence_loaded')
    finish
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

function! UpdatePresence()
    python3 vimsence.update_presence()
endfunction

function! DiscordReconnect()
    python3 vimsence.reconnect()
endfunction

command! -nargs=0 UpdatePresence call UpdatePresence()

augroup DiscordPresence
    autocmd!
    autocmd BufNewFile,BufRead,BufEnter * :call UpdatePresence()
augroup END

let g:vimsence_loaded = 1
