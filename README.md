# CURRENT STATUS
This project is paused because the FED of St. Louis website (for example, https://fred.stlouisfed.org/series/TOTALSA) achieves my goal. I may revive this project in the future if I need something more than what FED website can provide. 

# OVERVIEW

This repo provides a crawler and displays key economic indicator in a simple frontend.
This dashboard is inspired by the following sources:
* Bloomberg Eco Indicator Dashboard: https://www.bloomberg.com/graphics/world-economic-indicators-dashboard/?embedded-checkout=false 

# REQUIRED PACKAGES 
The backend is built with Python3. All packages are managed by pip. To install pip, do
```
brew install pip3
```

It's recommended to have a virtual environment to manage this. To create a virtual environment and install needed packages, do
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

# RUNNING THE APP

The app consists of a backend and a frontend. The backend is based on Flask. You can run Flask with this command:
```
./run_server.sh
```

The frontend has a simple html. You can use the built-in python server to run it. 
```
./run_frontend.sh
```

# ACESSING THE APP
For now, you should be able to see the app via 
```
localhost:8000
```
We are working on hosting the app on a public domain soon.
