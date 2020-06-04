" Closes if vim does not have python3
if !has('python3')
    echo 'Vim has to be compiled with +python3.'
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

let s:vimsence_has_timers = has("timers")
let s:timer = -1
let s:vimsence_init=0

" This loads the main dependencies and appends to the system path
python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
EOF

" Async init of vimsence. Should prevent Vim from starting slowly
function! s:InitializeDiscord()
    if s:vimsence_init
        return
    endif
    python3 import vimsence
    let s:vimsence_init=1
endfunction

function! DiscordAsyncWrapper(callback)
    if s:vimsence_has_timers
        if s:timer != -1
            " Timer protection; this avoids issues when double events are
            " dispatched.
            " This exists purely to avoid issuing several timers as a result
            " of the autocmd detecting file changes. (see the bottom
            " of this script). Time timer is so low that it shouldn't
            " interfere with several commands being dispatched at once.
            let info = timer_info(s:timer)
            if len(info) == 1 && info[0]["paused"] == 0
                " The timer is running; skip.
                return
            endif
        endif
        " Start the timer to dispatch the event
        let s:timer = timer_start(100, a:callback)
    else
        " Fallback; no timer support, call the function directly.
        call a:callback(0)
    endif
endfunction

" Note on the next functions with a tid argument:
" tid is short for timer id, and it's automatically
" passed to timer callbacks.
function! DiscordUpdatePresence(tid)
    call s:InitializeDiscord()
    python3 vimsence.update_presence()
    let s:timer = -1
endfunction

" Reconnect the discord rich presence
function! DiscordReconnect(tid)
    call s:InitializeDiscord()
    python3 vimsence.reconnect()
    let s:timer = -1
endfunction

" Disconnect the discord rich presence
function! DiscordDisconnect(tid)
    call s:InitializeDiscord()
    python3 vimsence.disconnect()
    let s:timer = -1
endfunction

" Register the vim commands
command! -nargs=0 UpdatePresence echo "This command has been deprecated. Use :DiscordUpdatePresence instead."
command! -nargs=0 DiscordUpdatePresence call DiscordAsyncWrapper(function('DiscordUpdatePresence'))
command! -nargs=0 DiscordReconnect call DiscordAsyncWrapper(function('DiscordReconnect'))
command! -nargs=0 DiscordDisconnect call DiscordAsyncWrapper(function('DiscordDisconnect'))

augroup DiscordPresence
    autocmd!
    autocmd BufNewFile,BufRead,BufEnter * :call DiscordAsyncWrapper(function('DiscordUpdatePresence'))
augroup END

" Set loaded to true
let g:vimsence_loaded = 1
