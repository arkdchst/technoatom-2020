#!/usr/bin/env bash

outfile=analyzed

print_usage(){
	cat <<EOF
usage: analyze.sh  task_a | task_b | task_c | task_d | task_e  <FILE> | <DIR>

task_a, task_b, task_c, task_d, task_e
	см. в README.md
FILE
	входной файл
DIR
	использовать рекурсивно файлы из DIR

Имя выходного файла - $outfile.
EOF
}


error(){
	if [ $# -ne 0 ]; then exit $1; fi
	exit 1
}


methods='^(OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT)$'

if [ ! $# -eq 2 ]; then
	print_usage
	error
fi

for last_arg in $@; do :; done
if [ -f $last_arg ]; then
	file="$last_arg"
elif [ -d $last_arg ]; then
	file=$(find "$last_arg" -type f)
	test -z "$file" && error
else
	echo 'No such file or directory' >&2
	error 2
fi

if [ -f analyzed ]; then
	echo -n "File '$outfile' exists, overwrite? (yes/NO): " >&2
	read answer
	if [ ! \( "$answer" = "y" -o "$answer" = "yes" \) ]; then	
		error 17
	fi
fi

exec 1>$outfile

case "$1" in
	--help)
		print_usage;;
	task_a)
		cat $file | wc -l
		;;
	task_b)
		cat $file | awk -F '[ "]' '{print $7}' | sort | grep -E $methods | uniq -c | sort -rg | awk '{print $2,$1}'
		;;
	task_c)
		cat $file | awk -F '[ "]' '{print $12,$11,$8}' | sort -k 3,3 -k 1,1rn | uniq -c -f 2 | sort -k 2,2rn | head -10 | awk '{print $4,$3,$1}'
		;;
	task_d)
		cat $file | awk -F '[ "]' '$11>=400 && $11<500 {print $11,$1,$8}' | sort -k 3,3 | uniq -c -f 2 | sort -k 1,1rn | head -10 | awk '{print $4,$2,$3}'
		;;
	task_e)
		cat $file | awk -F '[ "]' '$11>=500 && $11<600 {print $12,$8,$11,$1}' | sort -rnk 1,1 | head -10 | cut -d ' ' -f 2-
		;;
	*)
		rm $outfile
		print_usage >&2
		error
		;;
esac