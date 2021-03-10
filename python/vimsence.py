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
if (vim.eval("exists('{}')".format("g:vimsence_small_text")) == "1"):
    small_text = vim.eval("g:vimsence_small_text")
if (vim.eval("exists('{}')".format("g:vimsence_small_image")) == "1"):
    small_image = vim.eval("g:vimsence_small_image")

start_time = int(time.time())
base_activity = {
    'details': 'Nothing',
    'state': '',
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
if (vim.eval("exists('{}')".format("g:vimsence_client_id")) == "1"):
    client_id = vim.eval("g:vimsence_client_id")

# Contains which files has thumbnails.
has_thumbnail = {
    'c', 'cr', 'hs', 'json', 'nim', 'ruby', 'cpp', 'go', 'javascript', 'markdown',
    'typescript', 'python', 'vim', 'rust', 'css', 'html', 'vue', 'paco', 'tex', 'sh',
    'elixir', 'cs', 'f', 'jsx', 'tsx', 'sql', 'plsql', 'ocaml'
}

# Remaps file types to specific icons.
# The key is the filetype, the value is the image name.
# This is mainly used where the file type itself doesn't
# match the name of the thumbnail.
# Python files for an instance have the .py extension,
# Vim says the `:echo &filetype` is python,
# and the discord application uses the name "py"
# to represent the thumbnail.
remap = {
        "python": "py",
        "markdown": "md",
        "ruby": "rb",
        "rust": "rs",
        "typescript": "ts",
        "javascript": "js",
        "snippets": "vim",
        "typescriptreact": "ts",
        "javascriptreact": "js",
        "ocaml": "ml",
        "fortran": "f",
}

# Support for custom clients with icons
# vimsence_custom_icons is a mapping with the file types
# as the keys and their remapping which is the actual
# name of the thumbnail as the values.
if vim.eval("exists('g:vimsence_custom_icons')") == "1":
    thumbnails = vim.eval("g:vimsence_custom_icons")
    has_thumbnail.update(thumbnails.values())
    remap.update(thumbnails)

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
        return
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
    filedir = get_filedir()
    filetype = get_filetype()
    filesize = get_filesize()
    filesizeb = get_filesizeb()
    fileline = get_fileline()

    # Replace function for customization by user,
    # not a good code but it's fast and does the job
    def replace_text(string):
        string = string.replace("{filename}", filename)
        string = string.replace("{directory}", directory)
        string = string.replace("{filedir}", filedir)
        string = string.replace("{filetype}", filetype)
        string = string.replace("{filesize}", filesize)
        string = string.replace("{filesizeb}", filesizeb)
        string = string.replace("{fileline}", fileline)
        return string

    editing_text = 'Editing a {filetype} file'
    if (vim.eval("exists('{}')".format("g:vimsence_editing_text")) == "1"):
        editing_text = vim.eval("g:vimsence_editing_text")
    large_text = replace_text(editing_text)

    editing_text = 'Editing a {} file'
    if (vim.eval("exists('{}')".format("g:vimsence_editing_large_text")) == "1"):
        editing_text = vim.eval("g:vimsence_editing_large_text")

    editing_state = 'Workspace: {}'
    if (vim.eval("exists('{}')".format("g:vimsence_editing_state")) == "1"):
        editing_state = vim.eval("g:vimsence_editing_state")
    state = replace_text(editing_state)

    editing_details = 'Editing {filename}'
    if (vim.eval("exists('{}')".format("g:vimsence_editing_details")) == "1"):
        editing_details = vim.eval("g:vimsence_editing_details")
    details = replace_text(editing_details)

    if (u.contains(ignored_file_types, filetype) or u.contains(ignored_directories, directory)):
        # Priority #1: if the file type or folder is ignored, use the default activity to avoid exposing
        # the folder or file.
        rpc_obj.set_activity(base_activity)
        return
    elif filetype and (filetype in has_thumbnail or filetype in remap):
        # Check for files with thumbnail support
        large_text = replace_text(editing_text)
        if (filetype in remap):
            filetype = remap[filetype]

        large_image = filetype
    elif filetype in file_explorers or u.contains_fuzzy(file_explorer_names, filename):
        # Special case: file explorers. These have a separate icon and description.
        large_image = 'file-explorer'
        if (vim.eval("exists('{}')".format("g:vimsence_file_explorer_image")) == "1"):
            large_text = vim.eval("g:vimsence_file_explorer_image")

        large_text = 'In the file explorer'
        if (vim.eval("exists('{}')".format("g:vimsence_file_explorer_text")) == "1"):
            large_text = vim.eval("g:vimsence_file_explorer_text")

        details = 'Searching for files'
        if (vim.eval("exists('{}')".format("g:vimsence_file_explorer_details")) == "1"):
            details = vim.eval("g:vimsence_file_explorer_details")

        if (vim.eval("exists('{}')".format("g:vimsence_file_explorer_state")) == "1"):
            state = vim.eval("g:vimsence_file_explorer_state")
    elif (is_writeable() and filename):
        # if none of the other match, check if the buffer is writeable. If it is,
        # assume it's a file and continue.
        large_image = 'none'
        if (vim.eval("exists('{}')".format("g:vimsence_unknown_image")) == "1"):
            large_image = vim.eval("g:vimsence_unknown_image")

        large_text = replace_text(editing_text) if filetype else "Unknown" if not get_extension() else get_extension()
    else:
        large_image = 'none'
        if (vim.eval("exists('{}')".format("g:vimsence_idle_image")) == "1"):
            large_image = vim.eval("g:vimsence_idle_image")

        large_text = 'Nothing'
        details = 'Nothing'
        if (vim.eval("exists('{}')".format("g:vimsence_idle_text")) == "1"):
            large_text = vim.eval("g:vimsence_idle_text")
            details = vim.eval("g:vimsence_idle_text")

        if (vim.eval("exists('{}')".format("g:vimsence_idle_state")) == "1"):
            state = vim.eval("g:vimsence_idle_state")

    # Update the activity
    activity['assets']['large_image'] = large_image
    activity['assets']['large_text'] = large_text
    activity['details'] = details
    activity['state'] = state

    try:
        rpc_obj.set_activity(activity)
    except BrokenPipeError:
        # Connection to Discord is lost
        pass
    except NameError:
        # Discord is not running
        pass
    except OSError:
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

    return vim.eval('expand("%:e")')

def get_directory():

    """Get current directory
    :returns: string
    """

    return re.split(r"[\\/]", vim.eval('getcwd()'))[-1]

def get_filedir():

    """Get current file directory, fallback to get_directory() if errors
    :returns: string
    """

    try:
        dir = re.split(r"[\\/]", vim.eval('expand("%:p")'))[-2]
    except:
        dir = get_directory()

    return dir

def get_filesize():

    """Get current file human-readable size
    :returns: string
    """

    size = float(vim.eval('getfsize(expand(@%))'))
    if size <= 0:
        return "0B"
    names = ("B", "KB", "MB", "GB")
    i = 0
    while size > 1024.0:
        size = size / 1024.0
        i += 1
    return "%.1f%s" % (size, names[i])

def get_filesizeb():

    """Get current file size in bytes
    :returns: string
    """

    return vim.eval('getfsize(expand(@%))')

def get_fileline():

    """Get current file lines
    :returns: string
    """
    
    return vim.eval('line("$")')
