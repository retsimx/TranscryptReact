# Transcrypt React Webpack Example

---

This example is a basic demonstration of how Transcrypt can be used as a viable transpiler for programming a React web application. It takes advantage of webpack, and a custom watcher that listens to python file changes and manages the transpilation, and eventually the emission of the webpack module for use during development.

This is more a proof of concept that can be extended and used as the basis of a project.

## Setting up the project

### Requirements

* Python 3.6
* NodeJS (for `npm`)

### Installation

Follow the basic steps below to set up the environment for the project.

* Check out the code of the project
  * `git clone https://github.com/retsimx/TranscryptReact.git`
* Change to the `TranscryptReact` folder
  * `cd TranscryptReact`
* Create a virtual environment in the root of the project for Transcrypt. This virtual environment must be in a folder named `.venv`, I have used Python 3.6, other versions may work.
  * `virtualenv -p python3.6 .venv`
* Activate the virtual environment and install Transcrypt
  * `. .venv/bin/activate`
  * `pip install transcrypt`
* Install the required NodeJS packages
  * `npm install`

### Run development server

Run `npm run start` and visit `localhost:8080` in your browser.



### Produce production build

Run `npm run build` and the produced minified bundle will be emitted in to the `./build` folder as `app.js`



## Basic concept

The basic dev server consists of two separate phases. In the first phase, any changes to files within the `src` directory that are not in the `src/__target__` directory trigger Transcrypt to rebuild the `index.py` file. This results in the transpiled javascript files being emitted in to the `src/__target__` folder. The main webpack watcher then watches for changes in javascript files within the `src/__target__` folder, and then processes it's hotloading/bundling.



In the build phase, the webpack config will run a single build phase for transpiling the Transcrypt to javascript, and then processes the emitted javascript to in to a minified bundle.

