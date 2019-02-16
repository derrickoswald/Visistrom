/**
 * Javascript file for Page 2 of Open Energy Data Hack Days Vis1strom application.
 */
"use strict";
define
(
    ["mustache", "data"],
    function (mustache, dat)
    {
        /**
         * Pad a string on the left to width with padding.
         */
        function pad (width, string, padding)
        {
            return ((width <= string.length) ? string : pad (width, padding + string, padding));
        }

        function render ()
        {
            var data = dat.get_data ();
            var reference = dat.get_reference ();
            var template = `
                <div class="row">
                    <div class="col">
                    <ul class="forecast">
                        {{#days}}
                        <li>
                        <div class="row">
                        <div class="col-2">
                            {{time}}
                        </div>
                        <div class="col-5">
                            <img id="light-bulb-icon" class="forecast" src={{icon}} alt="light-bulb  status" width="100">
                        </div>
                        <div class="col-5">
                            <img id="light-bulb-icon" class="forecast" src={{tomorrow_icon}} alt="light-bulb  status" width="100">
                        </div>
                        </row>
                        </li>
                        {{/days}}
                    </ul>
                    </div>
                </div>
            `;

            var now = dat.pseudo_now ();
            var days = [];
            var count = 0;
            for (var property in data)
                if (reference.hasOwnProperty (property))
                {
                    var date = new Date (property);
                    if (date > now)
                    {
                        var tomorrow = new Date (date.valueOf ());
                        tomorrow.setDate (tomorrow.getDate () + 1);
                        if (0 == date.getMinutes ())
                        {
                            var time = "" + pad (2, "" + date.getHours (), "0") + ":" + pad (2, "" + date.getMinutes (), "0");
                            days.push ({ "time": time, "icon": dat.icon_for (date), "tomorrow_icon": dat.icon_for (tomorrow) });
                            count++;
                            if (count > 24)
                                break;
                        }
                    }
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