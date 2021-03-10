<p align="center">
  <h1 align="center">VimSence</h1>
</p>

<p align="center">
  <img src="https://i.imgur.com/aL4g3nx.png" width="300">
  <img src="https://i.imgur.com/nrhZj4O.png" width="300">
</p>

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.
More help about the plugin itself can be found [here](doc/vimsence.txt).

### Prerequisites
You need to have Vim/NeoVim with Python3 support

### Added Features
#### Tags
Currently working in `editing_large_text`, `editing_state` and `editing_details`
- `{filename}` current file name with extension
- `{filetype}` current file extension
- `{filesize}` current file human-readable size (KB, MB, ..)
- `{filesizeb}` current file size in bytes
- `{fileline}` current file lines
- `{filedir}` current file folder

#### New Configurations
Tip: Hide `state` or `details` with double spaces '  '
- `g:vimsence_file_explorer_image` image for file explorer
- `g:vimsence_file_epxlorer_state` file explorer bottom text
- `g:vimsence_unknown_image` image if filetype doesn't have an icon
- `g:vimsence_idle_image` image if no file is open (idling?)
- `g:vimsence_idle_text` idle text applies to large_text and details
- `g:vimsence_idle_state` idle bottom text

#### Details
- Added `get_filedir()`, `get_filesize()`, `get_filesizeb()` and `get_fileline()`
- Changed `g:vimsence_editing_large_text` to `g:vimsence_editing_text`

### Installing
#### [Vim-Plug](https://github.com/junegunn/vim-plug)
1. Add `Plug 'hugolgst/vimsence'` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:PlugInstall`

#### [Vundle](https://github.com/VundleVim/Vundle.vim) or similar
1. Add `Plugin 'hugolgst/vimsence'` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:BundleInstall`

#### [NeoBundle](https://github.com/Shougo/neobundle.vim)
1. Add `NeoBundle 'hugolgst/vimsence'` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:NeoUpdate`

#### [Pathogen](https://github.com/tpope/vim-pathogen)
```sh
cd ~/.vim/bundle
git clone https://github.com/hugolgst/vimsence.git
```

#### Vim8 packages
```sh
git submodule add https://github.com/hugolgst/vimsence.git vimsence
```

## Configuration
You can configure the messages of VimSence in your `.vimrc` with these options:
```vim
let g:vimsence_client_id = '439476230543245312'
let g:vimsence_small_text = 'NeoVim'
let g:vimsence_small_image = 'neovim'
let g:vimsence_editing_large_text = '{filetype} file'
let g:vimsence_editing_details = 'Editing {filename}'
let g:vimsence_editing_state = 'Working on {directory}'
let g:vimsence_file_explorer_text = 'In NERDTree'
let g:vimsence_file_explorer_details = 'Looking for files'
let g:vimsence_custom_icons = {'filetype': 'iconname'}
```

## Authors
| Contributor                                                                                                                         | What has been done    |
|-------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| <img src="https://avatars.githubusercontent.com/anned20" height=30px align=center>   [Anne Douwe Bouma](https://github.com/anned20) | Original work         |
| <img src="https://avatars.githubusercontent.com/hugolgst" height=30px align=center>   [Hugo Lageneste](https://github.com/hugolgst) | Maintaining this fork |

See also the list of [contributors](https://github.com/hugolgst/vimsence/contributors) who participated in this project.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
