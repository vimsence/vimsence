import vim
import rpc
import time
import logging

start_time = int(time.time())
base_activity = {
        'details': 'Nothing',
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'small_text': 'Vim',
            'small_image': 'vim',
            'large_text': 'Vim',
            'large_image': 'vim'
        }
    }

client_id = '439476230543245312'

has_thumbnail = [
    'c', 'cr', 'hs', 'json', 'nim', 'rb', 'cpp', 'go', 'js', 'md', 'ts', 'py', 'vim', 'rs', 'css', 'html', 'vue'
]

try:
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    rpc_obj.set_activity(base_activity)
except Exception as e:
    # Discord is not running
    pass

def update_presence():
    """Update presence in Discord
    """
    activity = base_activity
    activity['details'] = get_filename()
    activity['assets']['large_text'] = 'Editing a {} file.'.format(get_extension())

    if get_extension() and get_extension() in has_thumbnail:
        activity['assets']['large_image'] = get_extension()
    elif get_filename() == 'vimfiler:default':
        activity['assets']['large_image'] = 'file-explorer'
    else:
        activity['assets']['large_image'] = 'none'

    try:
        rpc_obj.set_activity(activity)
    except BrokenPipeError as e:
        # Connection to Discord is lost
        pass
    except NameError as e:
        # Discord is not running
        pass

def get_filename():
    """Get current filename that is being edited
    :returns: string
    """
    return vim.eval('expand("%:t")')

def get_extension():
    """Get exension for file that is being edited
    :returns: string
    """
    return vim.eval('expand("%:e")')
