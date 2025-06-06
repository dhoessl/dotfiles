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
" PLUGIN MANAGER {{{
call plug#begin()
Plug 'tpope/vim-sensible'
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'junegunn/goyo.vim'
Plug 'vim-pandoc/vim-pandoc-syntax'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-repeat'
Plug 'scrooloose/syntastic'
Plug 'glench/vim-jinja2-syntax'
Plug 'bluz71/vim-moonfly-colors', { 'as': 'moonfly' }
Plug 'NLKNguyen/papercolor-theme'
Plug 'itchyny/lightline.vim'
Plug 'instant-markdown/vim-instant-markdown', {'for': 'markdown', 'do': 'yarn install'}
call plug#end()
" }}}
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
" NERDTree {{{
" Show lines in files
let g:NERDTreeFileLines=1
" Show hidden
let g:NERDTreeShowHidden=1
" Open NERDTree nexto the file
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * NERDTree | if argc() > 0 || exists("s:std_in") | wincmd p | endif
" Close NERDTree if its the only window
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif
" fix lightline on Nerdtree
augroup filetype_nerdtree
    au!
    au FileType nerdtree call s:disable_lightline_on_nerdtree()
    au WinEnter,BufWinEnter,TabEnter * call s:disable_lightline_on_nerdtree()
augroup END

fu s:disable_lightline_on_nerdtree() abort
    let nerdtree_winnr = index(map(range(1, winnr('$')), {_,v -> getbufvar(winbufnr(v), '&ft')}), 'nerdtree') + 1
    call timer_start(0, {-> nerdtree_winnr && setwinvar(nerdtree_winnr, '&stl', '%#Normal#')})
endfu
" }}}
" Instant Markdown {{{
filetype plugin on
"Uncomment to override defaults:
"let g:instant_markdown_slow = 1
"let g:instant_markdown_autostart = 0
"let g:instant_markdown_open_to_the_world = 1
"let g:instant_markdown_allow_unsafe_content = 1
"let g:instant_markdown_allow_external_content = 0
"let g:instant_markdown_mathjax = 1
"let g:instant_markdown_mermaid = 1
"let g:instant_markdown_logfile = '/tmp/instant_markdown.log'
"let g:instant_markdown_autoscroll = 0
"let g:instant_markdown_port = 8888
"let g:instant_markdown_python = 1
"let g:instant_markdown_theme = 'dark'
" }}}
" lightline {{{
" autocmd VimEnter * call lightline#update()
set noshowmode
" }}}
" backgroundcolor {{{
hi normal ctermbg=NONE
hi nontext ctermbg=NONE
"}}}
" Colorscheme {{{
" colorscheme badwolf
" colorscheme moonfly
set background=dark
colorscheme PaperColor
" }}}
" Key Mappings {{{
nmap <F1> :set invnumber invrelativenumber<CR>
nmap <F2> :SyntasticCheck<CR>
nmap <F3> :SyntasticReset<CR>
nmap <F4> gt
nmap <F5> gT
nmap <F6> :vertical resize +2<CR>
nmap <F8> :vertical resize -2<CR>
nmap <F9> :resize +2<CR>
nmap <F10> :resize -2<CR>
" }}}
