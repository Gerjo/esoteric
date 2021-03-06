
PATHS=(
	/usr/local 
	/usr/local/bin
	
	~/bin
	~/Library/Android/sdk/platform-tools
	~/Library/Android/sdk/tools
	~/Library/Android/sdk/tools/bin
	~/rubygems/bin
)

# add the paths one by one, if the exist
for P in "${PATHS[@]}"; do 
	if [ -d "$P" ]; then
		PATH=$PATH:$P
	fi
done

# otherwise it requires root to install gems
export GEM_HOME=~/rubygems

source ~/esoteric/git-prompt.sh

###
# Detect ZSH
###
if [[ "$SHELL" == "/bin/zsh" ]]; then
	
	ISZSH=true
	
	# git completion is build-in. Nice.
	autoload -Uz compinit && compinit
	
else
	ISZSH=false
fi

###
# Detect windows subsystem for linux
###
if grep -q Microsoft /proc/version 2>/dev/null; then
    ISWSL=true
else
    ISWSL=false
fi

export EDITOR=nano
export VISUAL=nano

export ANDROID_HOME=~/Library/Android/sdk/
# Add fancy colors to ls.
alias ls="ls -G"

# Show as list layout, with colors.
alias ll='ls -lG'

# Show as list layout, with colors, and hidden files.
alias la='ls -lGa'

# Extract a compressed tarball
alias untar='tar -zxvf'

if ! [ -x "$(command -v pico)" ]; then
    alias pico='nano'
fi

# Find out where gitx is installed on my system.
gitx_path=$(find ~/Applications /Applications -iname "gitx.app" -type d -maxdepth 1 2>/dev/null)


if ! [ -x "$(command -v mate)" ]; then
	CODE_PATH=/mnt/c/Users/Gerard/AppData/Local/Programs/Microsoft\ VS\ Code/Code.exe

	if [ -f "$CODE_PATH" ]; then
		mate() {
			if [ "$#" -lt 1 ]; then
				"$CODE_PATH"
			else
				"$CODE_PATH" $1
			fi
		}
	fi
fi

### 
# Open the given, or current, directory in gitx.
###
gitx() {

	if [[ "$ISWSL" == true ]] ; then

		# note - this opens in a new window each time.
		APP="/mnt/c/Program Files (x86)/GitExtensions/GitExtensions.exe"

		if [ "$#" -lt 1 ]; then
			$(nohup "${APP}" browse </dev/null >/dev/null 2>&1 &)
		else
			$(cd $1; nohup "${APP}" browse </dev/null >/dev/null 2>&1 &)
		fi
	else
		if [ "$#" -lt 1 ]; then
			${gitx_path}/Contents/Resources/gitx
		else
			${gitx_path}/Contents/Resources/gitx --git-dir=$1
		fi
	fi
}

### 
# Find the first xcode project in the current folder, or specified folder.
###
xcode() {
 
	if [ "$#" -lt 1 ]; then
		open $(find . -name "*.xcodeproj" -d -print -quit)
	else
		open $(find $1 -name "*.xcodeproj" -d -print -quit)
	fi
 
}

qfind() {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: no file to search for specified"
		return 1
	fi
	
	RES=$(find . -iname "$1" -not -path '*/\.*' | head -n 1)

	if [ -z "$RES" ]; then
	    echo $(find . -iname "$1*" -not -path '*/\.*' | head -n 1)
	else
		echo $RES
	fi
}

qopen() {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: no file to search for specified"
		return 1
	fi
	
	# First argument represents the file or pattern searched for
	FILE=$(qfind "$1")
	
	if [ -z "$FILE" ]; then
		echo "error: file not found"
		return 1
	fi
	
	return $(open $FILE) 
}

qmate() {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: no file to search for specified"
		return 1
	fi
	
	# First argument represents the file or pattern searched for
	FILE=$(qfind "$1")
	
	if [ -z "$FILE" ]; then
		echo "error: file not found"
		return 1
	fi
	
	return $(mate $FILE) 
}

### 
# Search for a file, and blame it. Anything specified after the first argument 
# is directly passed onto the git blame command.
###
blame() {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: did not specify a file name or pattern"
		return 1
	fi

	# Grab all but the first argument. This is later directly passed into
	# the git blame command.
	ARGS=${@:2}

	FILEPATH=$(qfind "$1")
	
	if [ -z "$FILEPATH" ]; then
		echo "error: file not found in current checkout"
		return 1
	fi
	
	# -c effectively removes file in which the line of code was introduced.
	git blame -c "$FILEPATH" $ARGS
}

###
# Crude way of measuring write speed
###
disk_write_speed() {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: no file specified"
		return 1
	fi
	
	if [ -f "$1" ]; then
		echo "error: file exists"
	fi
	
	res=$(dd if=/dev/zero of=$1 bs=1g count=1 && rm $1)
}

###
# Generate a random UTF-8 icon based on the current time of day.
###
get_random_utf_icon() {
	ICONS=("♤" "♙" "☚" "☋" "☍" "☧" "☏" "☇" "♇" "♫" "♆" "☈" "♅" 
           "♗" "♚" "♩" "♕" "☱" "♞" "♯" "☟" "☩" "♬" "♁" "♭" "☼" 
           "♧" "☜" "☉" "✐" "☌" "♘" "☛" "☒" "♔" "♛" "☽" "☨" "☭" 
           "☡" "☻" "♜" "☊" "★" "♢" "*" "♖" "♝" "♃" "✎" "☬" "♮" 
           "☫" "♡" "❥" "♪" "☤" "☾" "☥" "♄" "☞" )
		
	# WSL - right now - has a much smaller range of supported 
	# UTF8 characters.
	if [[ "$ISWSL" == true ]] ; then
		ICONS=("■" "±" "║" "©" "£" "░" "¤" "≡")
	fi

	RANDOM=$$$(date +%s)
	WINNER=${ICONS[$RANDOM % ${#ICONS[@]} ]}	
		
	echo ${WINNER}
}

###
# Return a red color when running as root, non-red otherwise.
###
get_icon_color() {
	if [ "$EUID" -ne 0 ]; then
		# Not root
    	echo "\[\033[0;37m\]"
	else
		# Running as root
		echo "\[\033[1;31m\]"
	fi
}

###
# Determine the hostname to show on prompt.
###
show_host() {
	echo "\[\033[0;37m\]\u\[\033[0;90m\]@\[\033[0;90m\]\h "
}

show_dir() {
	echo "\\W"
}

###
# Rebase if possible; otherwise merge.
###
rebase() {
	git stash -u && git fetch
	git rebase
	if ! [ $? -eq 0 ]; then
		echo "Rebase failed, merging instead"
		git rebase --abort
		git merge
		if ! [ $? -eq 0 ]; then
			echo "Fatal: Merge failed, aborting"
			git merge --abort
			return -1
		else
			echo "Merge successful"
		fi
	else
		echo "Rebase successful"
	fi
	git stash pop
}

###
# git pull; also include submodules.
###
gpa() {
    git pull --recurse-submodule
}


if [[ "$ISZSH" == true ]] ; then
	#for i in {1..256}; do print -P "%F{$i}Color : $i"; done;

	RED="%F{9}"
	GREEN="%F{70}"
	GRAY="%F{251}"
	DARKGRAY="%F{239}"
	WHITE="%F{256}"
	YELLOWGREEN="%F{184}"

	setopt PROMPT_SUBST
	export PROMPT="${GRAY}%n${DARKGRAY}@%m${GREEN} %1~%f%b${YELLOWGREEN}\$(__git_ps1)${WHITE} $(get_random_utf_icon) "

else
	export PS1="$(show_host)\[\033[32m\]$(show_dir)\[\033[33m\]\$(__git_ps1)$(get_icon_color) $(get_random_utf_icon) \[\033[00m\]"	
fi

#RPROMPT='[%F{yellow}%?%f]'

