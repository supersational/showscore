(function () {
    console.log("initial loading showscore.js")
    var python_options = $$python_options;
    var osmd_options = $$osmd_options;
    console.log("python_options", python_options)
    console.log("osmd_options", osmd_options)
    function loadOSMDLibrary() {
        return new Promise(function (resolve, reject) {

            // OSMD script has a 'define' call which conflicts with requirejs
            const _define = window.define; // save the define object 
            if (_define !== undefined) {
                window.define = undefined; // now the loaded script will ignore requirejs
            }
            const script = document.createElement('script');
            const offline_script = python_options.offline_script; // the entire library in a string

            // if python has given us an offline script to use:
            script.type = 'text/javascript';

            script.text = offline_script;
            console.log("appending offline script", script)
            document.body.appendChild(script); // browser will try to load the new script tag
            if (_define !== undefined) {
                window.define = _define;
            }

            // Use setTimeout to check if the script has loaded
            setTimeout(function () {
                if (typeof window.opensheetmusicdisplay !== 'undefined') {
                    console.log("LOADED");
                    resolve(opensheetmusicdisplay);
                } else {
                    reject("Script did not load properly.");
                    // reject(window.opensheetmusicdisplay)
                }
            }, 0);
        });
    }
    const renderScore = (opensheetmusicdisplay) => {
        console.log("loaded OSMD")

        var div_id = python_options.div_id;

        document.getElementById(div_id).innerHTML = '';

        let openSheetMusicDisplay = new opensheetmusicdisplay.OpenSheetMusicDisplay(div_id, osmd_options);
        openSheetMusicDisplay
            .load(python_options.xml_data) // this is replaced by the xml generated in python
            .then(
                function () {
                    console.log("rendering data")
                    try {
                        openSheetMusicDisplay.render();
                    } catch (error) {
                        document.getElementById(div_id).innerHTML = "<p style='color:red'>Error rendering data:" + error + "</p>"
                    }
                    // we could also remove this script tag to free up memory (would limit debugging though)
                    // const thisScriptTag = document.currentScript;
                    // thisScriptTag.parentNode.removeChild(thisScriptTag)
                    python_options = null;
                    osmd_options = null;
                }
            );
    }
    // make it non-blocking
    setTimeout(() => {
        if (window.opensheetmusicdisplay) {
            // console.log("already loaded")
            renderScore(window.opensheetmusicdisplay);
        } else {
            loadOSMDLibrary().then(renderScore);
        }
    }, 0)


})();
console.log("script: showscore.js")