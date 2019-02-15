
/**
 * Main javascript file for Open Energy Data Hack Days Vis1strom application
 */
"use strict";
requirejs
(
    ["read_data"],
    function (read_data)
    {
        function doit ()
        {
            function show (objects)
            {
                alert (JSON.stringify (objects, null, 4).substring (0, 2000));
            }
            read_data.load ("data/4weeks_MD_T1_MHF1.csv").then (show);
        };
        // initialize widgets
        document.getElementById ("light-bulb-icon").onclick = doit;
        document.getElementById ("forecast").onclick = function () { alert ("forecast"); };
        document.getElementById ("club").onclick     = function () { alert ("club"); };
        document.getElementById ("history").onclick  = function () { alert ("history"); };
        document.getElementById ("options").onclick  = function () { alert ("options"); };

        read_data
    }
);
