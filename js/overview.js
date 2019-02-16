/**
 * Javascript file for Page 1 of Open Energy Data Hack Days Vis1strom application.
 */
"use strict";
define
(
    ["read_data", "forecast"],
    function (read_data, forecast)
    {
        // fake user data
        var TheData;
        // fake electric distribution data
        var TheReference;

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

            function normalize ()
            {
                // normalize the data
                var sum = 0.0
                var count = 0;
                for (var property in TheData)
                    if (TheData.hasOwnProperty (property))
                    {
                        var x = TheData[property].power;
                        sum += x;
                        count++;
                    }
                var average = sum / count;

                var refsum = 0.0;
                var refcount = 0;
                for (var property in TheReference)
                    if (TheReference.hasOwnProperty (property))
                    {
                        var x = Number(TheReference[property].power);
                        refsum += x;
                        refcount++;
                    }
                var refaverage = refsum / refcount;

                var scale = average / refaverage;
                for (var property in TheReference)
                    if (TheReference.hasOwnProperty (property))
                    {
                        var x = TheReference[property].power;
                        TheReference[property].power = x * scale;
                    }
            }

            function initialize ()
            {
                function convert (objects)
                {
                    var new_objects = {};
                    for (var property in objects)
                        if (objects.hasOwnProperty (property))
                        {
                            var data = objects[property]
                            var average = Number(data.average);
                            var power = Number(data.power);
                            if (!isNaN (average) && !isNaN (power))
                                new_objects[new Date (property)] = { average: average, power: power };
                        }

                    return (new_objects);
                }

                /**
                 * Pad a string on the left to width with padding.
                 */
                function pad (width, string, padding)
                {
                    return ((width <= string.length) ? string : pad (width, padding + string, padding));
                }

                function clean (objects)
                {
                    var new_objects = {};
                    for (var property in objects)
                        if (objects.hasOwnProperty (property))
                        {
                            if ("" != property)
                            {
                                var s = property.split (" ");
                                var t = s[1].split (":");
                                var u = s[0].split ("/");
                                var v = u[2] + "-" + pad (2, u[0], "0") + "-" + pad (2, u[1], "0");
                                var w = v + " " + pad (2, t[0], "0") + ":" + t[1] + ":00";
                                var date = new Date (w);
                                var data = objects[property]
                                var power = Number(data["Verbrauch Kanton AG (kWh)"]);
                                if (!isNaN (power))
                                    new_objects[date] = { power: power };
                            }
                        }
                    return (new_objects);
                }
                read_data.load ("data/4weeks_MD_T1_MHF1.csv").then (
                    function (objects)
                    {
                        TheData = convert (objects);
                        read_data.load ("data/Canton_Argau_Consumption_2018.csv", ";").then (
                            function (objects)
                            {
                                TheReference = clean (objects);
                                normalize ();
                                console.log ("data loaded");
                            }
                        );
                    }
                );
            }

            function doit ()
            {
                forecast.render (TheData, TheReference);
            };

            // initialize widgets
            document.getElementById ("main").innerHTML = template;
            document.getElementById ("light-bulb-icon").onclick = doit;
            document.getElementById ("forecast").onclick = function () { set_status ("use"); };
            document.getElementById ("club").onclick     = function () { set_status ("save"); };
            document.getElementById ("history").onclick  = function () { set_status ("ok"); };
            document.getElementById ("options").onclick  = function () { set_status ("bogus"); };

            // initialize the data
            initialize ();

        };

        return (
            {
                render: render
            }
        );
    }
);
