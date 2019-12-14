export ANDROID_HOME=/Users/gerjo/Library/Android/sdk

PATHS=(
	#/opt/local/bin 
	/usr/local 
	/usr/local/bin
	
	#/usr/local/mysql/bin
	
	~/bin
	~/Library/Android/sdk/platform-tools
	~/Library/Android/sdk/tools
	~/Library/Android/sdk/tools/bin
	~/rubygems/bin
)

# Warn about paths not found. Generally indicative of something going wrong. 
# (e.g., android SDK changed its install dir.)
for P in "${PATHS[@]}"; do 
	if [ -d "$P" ]; then
		PATH=$PATH:$P
	else
		echo "nonexistent path '$P' could not be added to \$PATH"
	fi
done

# otherwise it requires root to install gems
export GEM_HOME=~/rubygems

source ~/esoteric/git-prompt.sh
source ~/esoteric/git-completion.bash

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

if ! [ -x "$(command -v PICO)" ]; then
    alias pico='nano'
fi

# Find out where gitx is installed on my system.
gitx_path=$(find ~/Applications /Applications -iname "gitx.app" -type d -maxdepth 1 2>/dev/null)

### 
# Open the given, or current, directory in gitx.
###
gitx() {
	if [ "$#" -lt 1 ]; then
		${gitx_path}/Contents/Resources/gitx
	else
		${gitx_path}/Contents/Resources/gitx --git-dir=$1
	fi
}

qfind() {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: no file to search for specified"
		return 1
	fi
	
	RES=$(find . -iname "$1" -not -path '*/\.*' | HEAD -n 1)

	if [ -z "$RES" ]; then
	    echo $(find . -iname "$1*" -not -path '*/\.*' | HEAD -n 1)
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
# Determine the hostname to show on prompt.
###
show_host() {
	echo "\u@\h "
}

export PS1="$(show_host)\[\033[32m\]\W\[\033[33m\]\$(__git_ps1)\[\033[00m\] ❤ "
