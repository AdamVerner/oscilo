
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
apt=get update
apt-get install -y libgtk-3-dev python3-gi-cairo python3-dev glade
python3 -m pip  install pycairo matplotlib pygobject numpy typing
