
/**
 * Main javascript file for Open Energy Data Hack Days Visistrom application.
 */
"use strict";
requirejs
(
    ["overview"],
    function (overview)
    {
        overview.render ();
    }
);
