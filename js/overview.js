/**
 * Javascript file for Page 1 of Open Energy Data Hack Days Vis1strom application.
 */
"use strict";
define
(
    ["read_data"],
    function (read_data)
    {
        function render ()
        {

            var template = `
                <div class="row">
                    <div id="status" class="col my-2">
                        <img id="light-bulb-icon" class="center_main" src="images/light-bulb.svg" alt="light-bulb  status">
                    </div>
                </div>
                <div class="row my-2">
                    <div class="col">
                        <button id="forecast" class="btn btn-primary btn-lg btn-block"  type="button" >My Realm</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col my-2">
                        <button id="club"     class="btn btn-secondary btn-lg btn-block"type="button" >My Club</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col my-2">
                        <button id="history"  class="btn btn-success btn-lg btn-block"  type="button" >My History</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col my-2">
                        <button id="options"  class="btn btn-info btn-lg btn-block"     type="button" >What can I do</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col my-2">
                        <button id="options"  class="btn btn-info btn-lg btn-block"     type="button" >Compare Appliances</button>
                    </div>
                </div>
            `;

            /**
             * Set status to one of "use", "save", "ok".
             */
            function set_status (status)
            {
                var icon = "images/light-bulb.svg";
                switch (status)
                {
                    case "use":
                        icon = "images/light-bulb-on.svg";
                        break;
                    case "save":
                        icon = "images/light-bulb-off.svg";
                        break;
                    case "ok":
                        icon = "images/light-bulb-on-half.svg";
                        break;

                }
                document.getElementById ("light-bulb-icon").src = icon;
            }

            function doit ()
            {
                function show (objects)
                {
                    var new_objects = {};
                    for (var property in objects)
                        if (objects.hasOwnProperty (property))
                            new_objects[new Date (property)] = objects[property];
                    alert (JSON.stringify (new_objects, null, 4).substring (0, 2000));
                }
                read_data.load ("data/4weeks_MD_T1_MHF1.csv").then (show);
            };

            // initialize widgets
            document.getElementById ("main").innerHTML = template;
            document.getElementById ("light-bulb-icon").onclick = doit;
            document.getElementById ("forecast").onclick = function () { set_status ("use"); };
            document.getElementById ("club").onclick     = function () { set_status ("save"); };
            document.getElementById ("history").onclick  = function () { set_status ("ok"); };
            document.getElementById ("options").onclick  = function () { set_status ("bogus"); };

        };

        return (
            {
                render: render
            }
        );
    }
);
