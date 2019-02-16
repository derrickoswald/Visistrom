/**
 * Javascript file for Page 2 of Open Energy Data Hack Days Vis1strom application.
 */
"use strict";
define
(
    ["mustache"],
    function (mustache)
    {
        /**
         * Pad a string on the left to width with padding.
         */
        function pad (width, string, padding)
        {
            return ((width <= string.length) ? string : pad (width, padding + string, padding));
        }

        function render (data, reference)
        {
            var template = `
                <div class="row">
                    <div class="col-4">
                    </div>
                    <div class="col-4">
                    <ul class="forecast">
                        {{#days}}
                        <li>
                        <img id="light-bulb-icon" class="center_main" src={{icon}} alt="light-bulb  status" width="100">
                        {{time}}
                        </li>
                        {{/days}}
                    </ul>
                    </div>
                    <div class="col-4">
                    </div>
                </div>
            `;

            var days = [];
            var count = 0;
            for (var property in data)
                if (reference.hasOwnProperty (property))
                {
                    var date = new Date (property);
                    var time = "" + pad (2, "" + date.getHours (), "0") + ":" + pad (2, "" + date.getMinutes (), "0");
                    var diff = reference[property].power - data[property].power;
                    var item;
                    if (diff > 0.2)
                        item = { "time": time, "icon": "images/light-bulb-on.svg" };
                    else if (diff < -0.2)
                        item = { "time": time, "icon": "images/light-bulb-off.svg" };
                    else
                        item = { "time": time, "icon": "images/light-bulb-on-half.svg" };
                    days.push (item);
                    count++;
                    if (count > 30)
                        break;
                }

            var list = { days: days }
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