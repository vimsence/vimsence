import vim
import rpc
import time
import re
import utils as u
import logging

logger = logging.getLogger(__name__)

# Get small text and images from vim config
small_text = 'Vim'
small_image = 'vim'
if (vim.eval("exists('{}')".format("g:vimsence_small_text") == "1"):
    small_text = vim.eval("g:vimsence_small_text")
if (vim.eval("exists('{}')".format("g:vimsence_small_image") == "1"):
    small_text = vim.eval("g:vimsence_small_image")

start_time = int(time.time())
base_activity = {
    'details': 'Nothing',
    'timestamps': {
        'start': start_time
    },
    'assets': {
        'small_text': small_text,
        'small_image': small_image,
    }
}

client_id = '439476230543245312'
# Get the application id from vim configuration if there is one
if (vim.eval("exists('{}')".format("g:vimsence_app_id")) == "1"):
    client_id = vim.eval("g:vimsence_app_id")

has_thumbnail = [
    'c', 'cr', 'hs', 'json', 'nim', 'ruby', 'cpp', 'go', 'javascript', 'markdown',
    'typescript', 'python', 'vim', 'rust', 'css', 'html', 'vue', 'paco', 'tex', 'sh'
]

# Remaps file types to specific icons.
remap = {
        "python": "py", 
        "markdown": "md", 
        "ruby": "rb", 
        "rust": "rs", 
        "typescript": "ts",
        "javascript": "js"
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
# pre-initialization to deal with artifacts from slow initialization
rpc_obj = None
try:
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    rpc_obj.set_activity(base_activity)
except Exception as e:
    # Discord is not running.
    # The session is initialized and can be re-used later.
    pass

def update_presence():

    """
    Update presence in Discord
    """

    if rpc_obj is None or not rpc_obj.connected:
        # If we're flagged as disconnected, skip all this processing and save some CPU cycles.
        return;
    global ignored_file_types
    global ignored_directories
    if (ignored_file_types == -1):
        # Lazy init
        if (vim.eval("exists('{}')".format("g:vimsence_ignored_file_types")) == "1"):
            ignored_file_types = vim.eval("g:vimsence_ignored_file_types")
        else:
            ignored_file_types = []
        if (vim.eval("exists('{}')".format("g:vimsence_ignored_directories")) == "1"):
            ignored_directories = vim.eval("g:vimsence_ignored_directories")
        else:
            ignored_directories = []

    activity = base_activity

    large_image = ""
    large_text = ""
    details = ""
    state = ""

    filename = get_filename()
    directory = get_directory()
    filetype = get_filetype()

    if (u.contains(ignored_file_types, filetype) or u.contains(ignored_directories, directory)):
        # Priority #1: if the file type or folder is ignored, use the default activity to avoid exposing
        # the folder or file.
        rpc_obj.set_activity(base_activity)
        return
    elif filetype and filetype in has_thumbnail:
        # Check for files with thumbnail support
        large_text = 'Editing a {} file'.format(filetype)
        if (filetype in remap):
            filetype = remap[filetype]

        large_image = filetype

        details = 'Editing {}'.format(filename)
        state = 'Workspace: {}'.format(directory)
    elif filetype in file_explorers or u.contains_fuzzy(file_explorer_names, filename):
        # Special case: file explorers. These have a separate icon and description.
        large_image = 'file-explorer'
        large_text = 'In the file explorer'
        details = 'Searching for files'
        state = 'Workspace: {}'.format(directory)
    elif (is_writeable() and filename):
        # if none of the other match, check if the buffer is writeable. If it is,
        # assume it's a file and continue.
        large_image = 'none'

        large_text = 'Editing a {} file'.format(filetype if filetype else "Unknown" if not get_extension() else get_extension())
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

# reconnects the presence
def reconnect():
    if rpc_obj is None:
        logger.error("The plugin hasn't connected yet")
        return
    if rpc_obj.reconnect():
        update_presence()

# disconnects the presence
def disconnect():
    if rpc_obj is None:
        logger.error("The plugin hasn't connected yet")
        return
    try:
        if rpc_obj.connected:
            rpc_obj.close()
    except:
        pass

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

def get_filetype():

    """Get the filetype for file that is being edited
    :returns: string
    """

    return vim.eval('&filetype')

def get_extension():

    """Get the extension for the file that is being edited.
    Currently serves as a fallback if the filetype is null, which can
    happen if the filetype is unrecognized and/or unsupported by
    Vim (this is usually only the case when there are no plugins
    or anything else that adds a filetype to an unrecognized extension)
    :returns: string
    """

    return vim.eval('expand("%:e")');

def get_directory():

    """Get current directory
    :returns: string
    """

    return re.split(r"[\\/]", vim.eval('getcwd()'))[-1]
