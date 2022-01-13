#!/usr/bin/env bash
# Simple installation script to make sure the latest version is in the user's PATH

thisName=update_publicip.py
destDir=~/scripts/

echo "Copying script to ${destDir} directory..."
if [ -e ${destDir}/${thisName} ]; then
  echo "File exists! Overwriting..."
fi
cp ${thisName} ${destDir}

echo && echo "Do NOT forget to customize the script with, for instance:"
echo "sed -i \"s/user@example.org/YOURNAME@YOUR.SITE/\" ~/scripts/${thisName}" && echo

echo "Done!"
