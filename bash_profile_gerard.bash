export ANDROID_HOME=/Users/gerjo/Library/Android/sdk

PATHS=(
	#/opt/local/bin 
	/usr/local 
	/usr/local/bin
	
	#/usr/local/mysql/bin
	
	~/bin
	~/Library/Android/sdk/platform-tools
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

source ~/esoteric/git-prompt.sh
source ~/esoteric/git-completion.bash

# Shorthand for finding a file.
alias qfind="find . -iname "

# Add fancy colors to ls.
alias ls="ls -G"

# Show as list layout, with colors.
alias ll='ls -lG'

# Show as list layout, with colors, and hidden files.
alias la='ls -lGa'

### 
# Search for a file, and blame it. Anything specified after the first argument 
# is directly passed onto the git blame command.
###
function blame {
	if [ "$#" -lt 1 ]; then
	    echo "fatal: did not specify a file name or pattern"
		return 0
	fi
	
	# First argument represents the file or pattern searched for
	FILE=$1
	
	# Grab all but the first argument. This is later directly passed into
	# the git blame command.
	ARGS=${@:2}
	
	# Search for files only, case insensitive. Ignore anything inside
	# hidden folders
	FILEPATH=$(find . -type f -iname $FILE -not -path '*/\.*'|head -n1)
	
	# -c effectively removes file in which the line of code was introduced.
	git blame -c $FILEPATH $ARGS
}

###
# Determine the hostname to show on prompt.
###
show_host() {
	echo "\u@\h "
}

export PS1="$(show_host)\[\033[32m\]\W\[\033[33m\]\$(__git_ps1)\[\033[00m\] ❤ "