
/**
 * Main javascript file for Open Energy Data Hack Days Visstrom application
 */
"use strict";
requirejs
(
    [],
    function ()
    {
        // initialize widgets
        document.getElementById ("light-bulb-icon").onclick = function () { alert ("hello world"); };
        document.getElementById ("forecast").onclick = function () { alert ("forecast"); };
        document.getElementById ("club").onclick     = function () { alert ("club"); };
        document.getElementById ("history").onclick  = function () { alert ("history"); };
        document.getElementById ("options").onclick  = function () { alert ("options"); };

//        cimmap.initialize ();
    }
);
