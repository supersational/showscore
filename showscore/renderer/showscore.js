// showscore/renderer/showscore.js

(function () {
    const python_options = $$python_options;
    const osmd_options = $$osmd_options;

    console.log("python_options", python_options)
    console.log("osmd_options", osmd_options)
    // This function loads the OSMD library from the string provided by Python
    function loadOSMDLibrary() {
        return new Promise(function (resolve, reject) {
            // OSMD script has a 'define' call which can conflict with requirejs in notebooks
            const _define = window.define;
            if (_define !== undefined) {
                window.define = undefined; // Temporarily disable AMD define
            }
            
            const script = document.createElement('script');
            script.type = 'text/javascript';
            script.text = python_options.offline_script;
            document.body.appendChild(script);

            if (_define !== undefined) {
                window.define = _define; // Restore it
            }

            // Check if the script has loaded successfully
            setTimeout(() => {
                if (window.opensheetmusicdisplay) {
                    resolve(window.opensheetmusicdisplay);
                } else {
                    reject("OpenSheetMusicDisplay library failed to load.");
                }
            }, 0);
        });
    }

    // This function initializes OSMD and renders the score
    const renderScore = (osmd) => {
        const div_id = python_options.div_id;
        const container = document.getElementById(div_id);
        if (!container) {
            console.error(`showscore.js: Could not find container element with id "${div_id}"`);
            return;
        }
        container.innerHTML = ''; // Clear previous content

        // OSMD base options: https://github.com/opensheetmusicdisplay/opensheetmusicdisplay/blob/c4209608320572c7875a21c99a5c263a14b45e17/src/OpenSheetMusicDisplay/OSMDOptions.ts#L21
        // OSMD EngravingRules: https://github.com/opensheetmusicdisplay/opensheetmusicdisplay/blob/c4209608320572c7875a21c99a5c263a14b45e17/src/MusicalScore/Graphical/EngravingRules.ts#L26

        const openSheetMusicDisplay = new osmd.OpenSheetMusicDisplay(container, osmd_options);

        if (osmd_options.EngravingRules) {
            for (const [key, value] of Object.entries(osmd_options.EngravingRules)) {
                console.log("setting", key, value, "previous", openSheetMusicDisplay.rules[key])
                openSheetMusicDisplay.rules[key] = value;
            }
            delete osmd_options.EngravingRules;
        }
        window.openSheetMusicDisplay = openSheetMusicDisplay; // For debugging access in console

        openSheetMusicDisplay
            .load(python_options.xml_data)
            .then(
                () => {
                    try {
                        openSheetMusicDisplay.render();
                    } catch (error) {
                        container.innerHTML = `<p style='color:red'>Error rendering score: ${error}</p>`;
                    }
                },
                (err) => {
                    container.innerHTML = `<p style='color:red'>Error loading score: ${err}</p>`;
                }
            );
    };

    // Main execution logic
    setTimeout(() => {
        if (window.opensheetmusicdisplay) {
            // OSMD is already loaded on the page, just render.
            renderScore(window.opensheetmusicdisplay);
        } else {
            // Load the library first, then render.
            loadOSMDLibrary().then(renderScore).catch(console.error);
        }
    }, 0);
})(); 