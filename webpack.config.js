const path = require('path');
const execSync = require('child_process').execSync;
const WebpackWatchPlugin = require('webpack-watch-files-plugin')['default'];

// The root python file that is the entry point for the application
const index_file = __dirname + "/src/index.py";

module.exports = (env, argv) => {
    function build_index_python() {
        // Execute transcrypt to transpile the index python file to javascript
        execSync('.venv/bin/transcrypt -b -n -m -e 6 ' + index_file, {stdio: [0, 1, 2]});
    }

    // Always execute the python build at startup to make sure the content in __target__ exists
    build_index_python();

    // Our Plugin that watches for any file changes in /src that are not in the __target__ directory, and than runs
    // transcrypt to retranspile the changes
    class BuildIndexPythonPlugin {
        getChangedFiles(compiler) {
            // Returns a list of files from the watcher that changed
            const {watchFileSystem} = compiler;
            const watcher = watchFileSystem.watcher || watchFileSystem.wfs.watcher;

            return Object.keys(watcher.mtimes);
        }

        apply(compiler) {
            // Listen on the watcher for any file changes
            compiler.hooks.watchRun.tapAsync('BuildIndexPythonPlugin', (_compiler, done) => {
                // Get the list of changed files
                const changedFile = this.getChangedFiles(_compiler);
                // Check that there were actually one or more changed files
                if (changedFile.length) {
                    // If no files that triggered the watch reside in the __target__ directory, then that means a python
                    // file in our source tree must have changed and we should rebuild the javascript from the python
                    // using transcrypt
                    let compile_python = true;
                    for (let file in changedFile) {
                        file = changedFile[file];
                        if (file.includes('__target__')) {
                            compile_python = false;
                        }
                    }

                    // Rebuild if no files that changed were in the __target__ directory
                    if (compile_python) {
                        build_index_python();
                    }
                }
                return done();
            });
        }
    }

    const debug = argv.mode !== 'production';

    return {
        entry: ["__target__/index.js"],
        output: {
            path: __dirname + "/dist",
            filename: "app.js"
        },

        optimization: debug ? {
            // We no not want to minimize our code.
            minimize: false
        } : {
            minimize: true,
            noEmitOnErrors: true,
        },

        resolve: {
            modules: [
                path.resolve(__dirname, "src"),
                "node_modules"
            ],
        },

        devtool: debug ? "inline-sourcemap" : null,

        devServer: {
            contentBase: [
                path.resolve(__dirname, 'build'),
                path.resolve(__dirname, 'src'),
            ],
            publicPath: '/',
            watchContentBase: true,
            watchOptions: {
                poll: true,
                hot: true,
                watch: true,
            },
        },

        plugins: debug ? [
            new WebpackWatchPlugin({
                files: [
                    './src/**/*.py',
                    '!./src/__target__/**/*'
                ],
            }),
            new BuildIndexPythonPlugin(),
        ] : [],
    }
}