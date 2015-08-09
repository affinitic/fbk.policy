#!/bin/sh
domain=fbk.policy

i18ndude rebuild-pot --pot $domain.pot --create $domain ../

declare -a languages=("nl" "fr" "en")
for lang in "${languages[@]}"; do
		mkdir -p $lang/LC_MESSAGES
done

for lang in $(find . -mindepth 1 -maxdepth 1 -type d); do
		if test -d $lang/LC_MESSAGES; then
				touch $lang/LC_MESSAGES/$domain.po
				i18ndude sync --pot $domain.pot $lang/LC_MESSAGES/$domain.po
		fi
done
