# set up virtualenv
which python3
if [ "$?" == "1" ]; then
    echo "python3 is not available"
    exit 1
fi

virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
