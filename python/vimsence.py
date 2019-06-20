import vim
import rpc
import time
import re
import utils as u

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
    'c', 'cr', 'hs', 'json', 'nim', 'rb', 'cpp', 'go', 'js', 'markdown', 'ts', 'python',
    'vim', 'rs', 'css', 'html', 'vue'
]
# Remaps file types to specific icons.
remap = { 
    "python": "py", "markdown": "md"
}

file_explorers = [
    "nerdtree", "vimfiler", "netrw"
]
# Fallbacks if, for some reason, the filetype isn't detected.
file_explorer_names = [
    "vimfiler:default", "NERD_tree_", "NetrwTreeListing"
]

ignored_file_types  = -1
ignored_directories = -1
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
    global ignored_file_types
    global ignored_directories
    if (ignored_file_types == -1):
        # Lazy init 
        ignored_file_types = vim.eval("g:vimsence_ignored_file_types")
        ignored_directories = vim.eval("g:vimsence_ignored_directories")
    
    activity = base_activity

    large_image = ""
    large_text = ""
    details = ""
    state = ""

    filename = get_filename()
    directory = get_directory()
    extension = get_extension()

    if (u.contains(ignored_file_types, extension) or u.contains(ignored_directories, directory)):
        # Priority #1: if the file type or folder is ignored, use the default activity to avoid exposing
        # the folder or file. 
        rpc_obj.set_activity(base_activity)
        return
    elif extension and extension in has_thumbnail:
        # Check for files with thumbnail support
        large_text = 'Editing a {} file'.format(extension)
        if (extension in remap):
            extension = remap[extension]

        large_image = extension

        details = 'Editing {}'.format(filename)
        state = 'Workspace: {}'.format(directory)
    elif extension in file_explorers or u.contains_fuzzy(file_explorer_names, filename):
        # Special case: file explorers. These have a separate icon and description.
        large_image = 'file-explorer'
        large_text = 'In the file explorer'
        details = 'Searching for files'
        state = 'Workspace: {}'.format(directory)
    elif (is_writeable() and filename):
        # if none of the other match, check if the buffer is writeable. If it is, 
        # assume it's a file and continue.
        large_image = 'none'
        large_text = 'Editing a {} file'.format(extension)
        details = 'Editing {}'.format(filename)
        state = 'Workspace: {}'.format(directory)
    else:
        large_image = 'none'
        large_text = 'Nothing'
        details = 'Nothing'

    # Update the activity 
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

def is_writeable():
    """Returns whether the buffer is writeable or not 
    :returns: string
    """
    return vim.eval('&modifiable')

def get_filename():
    """Get current filename that is being edited
    :returns: string
    """
    return vim.eval('expand("%:t")')

def get_extension():
    """Get exension for file that is being edited
    :returns: string
    """
    return vim.eval('&filetype')

def get_directory():
    """Get current directory
    :returns: string
    """
    return re.split(r"[\\/]", vim.eval('getcwd()'))[-1]
