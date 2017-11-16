if [[ $UID != 0 ]]; then
	echo "Please start the script as root or sudo!"
	exit 1
fi
chmod +x src/mongoinstall.sh
chmod +x src/virtualenv_setup.sh
./src/mongoinstall.sh
./src/virtualenv_setup.sh
