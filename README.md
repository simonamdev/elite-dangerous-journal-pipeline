# Elite: Dangerous Journal Pipeline

End to end system to pipe events from one or several Elite: Dangerous journals into a database for real time consumption.

## Aim

The original aim of EDJP was to be able to have a live updating ticker displayed in a browser source within an overlay
of a twitch stream during in-game events. EDJP is a working proof of concept of this, without the event specific assets.

## Stack

EDJP is structured as follows:

* Server: API in Python 3 using Flask and RethinkDB.
* Client: ES6 client side Javascript including build scripts to transpile and bundle for browsers using browserify and Gulp.
* App: Python 3 console application which watches for journal changes and sends them to the API.

## Requirements

* Python 3.* (tested against 3.5 and 3.6)
* NodeJS
* [RethinkDB](https://www.rethinkdb.com) (tested against 2.3.6)

## Demo

// TODO

## Usage

### Server

`cd server`

`pip3 install -r requirements.txt`

In a separate terminal/cmd, run: `rethinkdb`

`python3 api.py`

To test that the API is functional, access the following in your browser: http://localhost:5000/

### Client

`cd client`

`npm install`

`npm install -g gulp`

Run this to package and minify the client side files:
`gulp build`

Run the following to have the files copied for development use:
`gulp copy_dev`

For distribution, use this instead: `gulp copy`

### App

`cd app`

`pip3 install -r requirements.txt`

Run the following batch file: `build_exe.bat`. That should create an executable in the dist/ folder

`cd dist/`

Copy the config.json into the dist/ folder

Edit the details as required

Run the executable.

If everything is setup correctly, it should seek to the end of the current journal file and print events to console as they happen.
It will also begin to send events to the API.

If the API is setup correctly, you should be able to access `locahost:5000/overlay` and see the events update as they happen.


## Contributing

Pull Requests and Issues are welcome!

## Licence

MIT

## Disclaimer

"EDJP was created using assets and imagery from Elite Dangerous, with the permission of Frontier Developments plc, for non-commercial purposes. It is not endorsed by nor reflects the views or opinions of Frontier Developments and no employee of Frontier Developments was involved in the making of it."