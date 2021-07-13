<p align="center">
  <h1 align="center">VimSence</h1>
</p>

<p align="center">
  <img src="https://i.postimg.cc/8PvMZFvz/13-07-21-19-41-56.png" width="400">
</p>

**A fork of vimsence with much better looking icons, support of more languages and also gonna add `Open Repository` button**

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.
More help about the plugin itself can be found [here](doc/vimsence.txt).

### Prerequisites
You need to have Vim/NeoVim with Python3 support

### Installing
#### [Vim-Plug](https://github.com/junegunn/vim-plug)
1. Add `Plug 'anurag3301/vimsence'` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:PlugInstall`

#### [Vundle](https://github.com/VundleVim/Vundle.vim) or similar
1. Add `Plugin 'anurag3301/vimsence'` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:BundleInstall`

#### [NeoBundle](https://github.com/Shougo/neobundle.vim)
1. Add `NeoBundle 'anurag3301/vimsence'` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:NeoUpdate`

#### [Dein.vim](https://github.com/Shougo/dein.vim)
1. Add `call dein#add('anurag3301/vimsence')` to your vimrc file.
2. Reload your vimrc or restart
3. Run `:call dein#install()`

#### [Pathogen](https://github.com/tpope/vim-pathogen)
```sh
cd ~/.vim/bundle
git clone https://github.com/anurag3301/vimsence.git
```

#### Vim8 packages
```sh
git submodule add https://github.com/anurag3301/vimsence.git vimsence
```

## Configuration
You can configure the messages of VimSence in your `.vimrc` with these options:
```vim
let g:vimsence_client_id = '439476230543245312'
let g:vimsence_small_text = 'NeoVim'
let g:vimsence_small_image = 'neovim'
let g:vimsence_editing_details = 'Editing: {}'
let g:vimsence_editing_state = 'Working on: {}'
let g:vimsence_file_explorer_text = 'In NERDTree'
let g:vimsence_file_explorer_details = 'Looking for files'
let g:vimsence_custom_icons = {'filetype': 'iconname'}
```

## Development
First create a virtual environment.
If you don’t already have a preferred way to do this,
take some time to look at tools like pew, virtualfish, and virtualenvwrapper.

Install the development dependencies:
```sh
pip install -r requirements-dev.txt
```

To avoid committing code that violates our style guide, we strongly advise you to install [pre-commit](https://pre-commit.com/) hooks:
```sh
pre-commit install
```

You can also run them anytime using:
```sh
pre-commit run --all-files
```

## Authors
| Contributor                                                                                                                         | What has been done    |
|-------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| <img src="https://avatars.githubusercontent.com/hugolgst" height=30px align=center>   [Hugo Lageneste](https://github.com/hugolgst) | Original work         |

See also the list of [contributors](https://github.com/vimsence/vimsence/contributors) who participated in this project.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
