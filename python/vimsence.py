import vim
import rpc
import time
import logging
import re

start_time = int(time.time())
base_activity = {
        'details': 'Nothing',
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'small_text': 'Vim',
            'small_image': 'vim',
        }
    }

client_id = '439476230543245312'

has_thumbnail = [
    'c', 'cr', 'hs', 'json', 'nim', 'rb', 'cpp', 'hpp', 'go', 'js', 'md', 'ts', 'py',
    'vim', 'rs', 'css', 'html', 'vue'
]


try:
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    rpc_obj.set_activity(base_activity)
except Exception as e:
    # Discord is not running.
    # The session is initialized and can be re-used later.
    pass


def update_presence():
    """Update presence in Discord
    """
    activity = base_activity

    large_image = ""
    large_text = ""
    details = ""
    state = ""

    filename = get_filename()
    directory = get_directory()
    extension = get_extension()

    if extension and extension in has_thumbnail:
        if extension == "hpp":
            large_image = "cpp"
        else:
            large_image = extension
        large_text = 'Editing a {} file'.format(extension)
        details = 'Editing {}'.format(filename)
        state = 'Workspace: {}'.format(directory)
    elif filename.startswith("."):
        if filename in has_thumbnail:
            large_image = filename
        else:
            large_image = "none"
        large_text = 'Editing a {} file'.format(filename)
        details = 'Editing {}'.format(filename)
        state = 'Workspace: {}'.format(directory)
    elif filename == 'vimfiler:default' or "NERD_tree_" in filename or "NetrwTreeListing" in filename:
        large_image = 'file-explorer'
        large_text = 'In the file explorer'
        details = 'Searching for files'
        state = 'Workspace: {}'.format(directory)
    else:
        large_image = 'none'
        large_text = 'Nothing'
        details = 'Nothing'

    activity['assets']['large_image'] = large_image
    activity['assets']['large_text'] = large_text
    activity['details'] = details
    activity['state'] = state

    try:
        rpc_obj.set_activity(activity)
    except BrokenPipeError as e:
        # Connection to Discord is lost
        pass
    except NameError as e:
        # Discord is not running
        pass
    except OSError as e:
        # IO-related issues (possibly disconnected)
        pass

def reconnect():
    if rpc_obj.reconnect():
        update_presence()

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

def get_directory():
    """Get current directory
    :returns: string
    """
    return re.split(r"[\\/]", vim.eval('getcwd()'))[-1]
