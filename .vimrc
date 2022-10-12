colorscheme badwolf
" Section 1 {{{
set autoindent
set smartindent
set shiftwidth=2
set tabstop=2
set softtabstop=2
set expandtab
set list
" }}}
" Section 2 {{{
set showcmd
set wildmode=longest,list,full
set wildmenu
filetype off
filetype plugin indent on
syntax on
set incsearch
set hlsearch
" }}}
" {{{ Klaus Dinge
set nocompatible
set nobackup
set ruler
" }}}
" Foldsection {{{
set foldenable
set foldlevelstart=0
set foldnestmax=10
set foldmethod=marker
nnoremap <space> za
"}}}
" Highlighting {{{
hi CursorLine cterm=bold term=bold
hi LineNr ctermfg=lightblue ctermbg=black cterm=none
set cursorline
"}}}
" Syntastic {{{
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_exit = 0
let g:syntastic_check_on_wq = 0
let g:syntastic_python_checkers = ['flake8']
let g:syntastic_yaml_checkers = ['yamllint']

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_loc_list_height = 3
"}}}
" backgroundcolor {{{
hi normal ctermbg=NONE
hi nontext ctermbg=NONE
"}}}
" PLUGIN MANAGER {{{
call plug#begin()
Plug 'tpope/vim-sensible'
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'junegunn/goyo.vim'
Plug 'vim-pandoc/vim-pandoc-syntax'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-repeat'
Plug 'scrooloose/syntastic'
call plug#end()
"}}}
" Key Mappings {{{
nmap <F1> :set invnumber invrelativenumber<CR>
nmap <F2> :SyntasticCheck<CR>
nmap <F3> :SyntasticReset<CR>
nmap <F4> :tabnew
nmap <F5> gt
nmap <F6> gT
nmap <F8> :tabm -1
nmap <F9> :tabm +1
nmap <F10> :q!
" }}}
