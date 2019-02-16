/**
 * CSV reading functions for Visistrom.
 */
"use strict";
define
(
    [],
    /**
     * @summary Reads a csv file.
     * @description Provides a set of objects mapped from the lines of the CSV.
     * @name read_data
     * @exports read_data
     * @version 1.0
     */
    function ()
    {
        function load (file_name, delimiter)
        {
            delimiter = delimiter || ",";

            function process (csv)
            {
                var allTextLines = csv.split (/\r\n|\n/);
                var headers = allTextLines[0].split (delimiter);
                var lines = {};
                for (var i = 1; i < allTextLines.length; i++)
                {
                    var data = allTextLines[i].split (delimiter);
                    var key = data[0];
                    var obj = {};
                    for (var j = 1; j < headers.length; j++)
                    {
                        obj[headers[j]] = data[j];
                    }
                    lines[key] = obj;
                }
                return (lines);
            }

            return new Promise (
                 function (resolve, reject)
                 {
                     var xhr = new XMLHttpRequest();
                     xhr.open ("GET", file_name);
                     xhr.onload = function ()
                     {
                         if (this.status >= 200 && this.status < 300)
                         {
                             resolve (process (xhr.response));
                         }
                         else
                         {
                             reject (
                                 {
                                     status: this.status,
                                     statusText: xhr.statusText
                                 }
                             );
                         }
                     };
                     xhr.onerror = function ()
                     {
                         reject (
                             {
                                 status: this.status,
                                 statusText: xhr.statusText
                             }
                         );
                     };
                     xhr.send();
                 }
            );
        }

        return (
            {
                load: load
            }
        );
    }
);
