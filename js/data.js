/**
 * Javascript file for Page 1 of Open Energy Data Hack Days Vis1strom application.
 */
"use strict";
define
(
    ["read_data"],
    function (read_data)
    {
        // fake user data
        var TheData;
        // fake electric distribution data
        var TheReference;

        function recommendation_for (time)
        {
            var ret;

            var diff = TheReference[time].power - TheData[time].power;
            if (diff > 0.2)
                ret = "use";
            else if (diff < -0.2)
                ret = "save";
            else
                ret = "ok";

            return (ret);
        }

        function icon_for (time)
        {
            var ret;

            switch (recommendation_for (time))
            {
                case "use":
                    ret = "images/light-bulb-on.svg"
                    break;
                case "save":
                    ret = "images/light-bulb-off.svg"
                    break;
                case "ok":
                    ret = "images/light-bulb-on-half.svg"
                    break;
            }

            return (ret);
        }

        function get_data ()
        {
            return (TheData);
        }

        function get_reference ()
        {
            return (TheReference);
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

        return (
            {
                initialize: initialize,
                recommendation_for: recommendation_for,
                icon_for: icon_for,
                get_data: get_data,
                get_reference: get_reference
            }
        );
    }
);