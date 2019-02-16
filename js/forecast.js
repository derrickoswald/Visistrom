/**
 * Javascript file for Page 2 of Open Energy Data Hack Days Vis1strom application.
 */
"use strict";
define
(
    ["mustache"],
    function (mustache)
    {
        function render ()
        {
            var template = `
                <div class="row">
                    <div class="col-4">
                    </div>
                    <div class="col-4">
                    <ul class="forecast">
                        {{#days}}
                        <img id="light-bulb-icon" class="center_main" src={{icon}} alt="light-bulb  status" width="100">
                        {{/days}}
                    </ul>
                    </div>
                    <div class="col-4">
                    </div>
                </div>
            `;
            var list = { days: [
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on.svg" },
                { "icon": "images/light-bulb-off.svg" },
                { "icon": "images/light-bulb-on.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                { "icon": "images/light-bulb-on-half.svg" },
                ] }
            var html = mustache.render (template, list);
            document.getElementById ("main").innerHTML = html;
        }

        return (
            {
                render: render
            }
        );
    }
);