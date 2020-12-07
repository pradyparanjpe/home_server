// -*- coding: utf-8; mode: javascript; -*-
// Copyright 2020 Pradyumna Paranjape
/* coding:utf-8; mode: javascript */
/*
 * Copyright 2020 Pradyumna Paranjape
 * This file is part of prady_web_land.
 *
 * prady_web_land is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * prady_web_land is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with prady_web_land.  If not, see <https://www.gnu.org/licenses/>.
 */

// Add places in format city: StateCode
// Expected weather details
var weatherDetails = {
    'name': '',
    'temp': '',
    'partOfDay': '\u{2600}'.fontcolor("yellow"), // Default: Sun
    'desc': '',
};


if ((typeof display === 'undefined') || Object.keys(display).length === 0) {
    console.log("display is empty, setting placeholders of my own");
    var display =
    {
        appID: "TO BE CREATED",
        places: {},
        searchTitle: "SEARCH",
        searchTerm: "GO",
        searchEngine: "http://www.google.com",
        quicklinkSet: {
            "COLUMN 1": {
                google: "https://www.google.com",
            },
        }
    };
}

// Blocking XML http request
function makeRequest(method, url) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send();
    });
}

// Parse NowCast from API This will have to change when API changes
async function parseWeather(cityName, loc) {
    let weatherURL = 'https://api.openweathermap.org'
        + '/data/2.5/weather'
        + '?q=' + cityName + ',' + loc
        + '&units=metric'
        + '&appid=' + display["appID"];
    let responseText = await makeRequest('GET', weatherURL);
    let nowCast = await JSON.parse(responseText);
    weatherDetails['name'] = nowCast.name;
    weatherDetails['temp'] = nowCast.main.temp.toFixed(1) + "\u{2103}";
    weatherDetails['desc']= nowCast.weather[0].description;
    if (nowCast.dt < nowCast.sys.sunrise || nowCast.dt >= nowCast.sys.sunset) {
        weatherDetails['partOfDay'] = '\u{1f319}'.fontcolor("#00cfff");
    };
}

// Loop to query owm for each city
async function setCityWeather(places) {
    let statDiv, cityLine, city, stat;
    let weatherCont = await document.getElementById("weather");
    while (weatherCont.firstChild) {
        weatherCont.removeChild(weatherCont.firstChild);
    };
    for (city in places) {
        if (places.hasOwnProperty(city)) {
            cityLine = document.createElement('div');
            cityLine.setAttribute('class', 'city');
            await parseWeather(city, places[city]);
            weatherDetails['name'] += ":";
            for (stat in weatherDetails) {
                if (weatherDetails.hasOwnProperty(stat)) {
                    statDiv = document.createElement('div');
                    statDiv.setAttribute('class', 'inline');
                    statDiv.innerHTML = weatherDetails[stat];
                    cityLine.appendChild(statDiv);
                }
            }
            weatherCont.appendChild(cityLine);
        };
    };
}

// A searx event must be hosted for this to work
async function callSearx() {
    let val = document.getElementById("search-field").value;
    if (val)
        window.open(display["searchEngine"] + 'search?q=' + val);
}

// Toggle search field
async function toggleSearch() {
    if (document.getElementById('search').style.display == 'flex') {
        document.getElementById('search-field').value = '';
        document.getElementById('search-field').blur();
        document.getElementById('search').style.display = 'none';
    } else {
        document.getElementById('search').style.display = 'flex';
        document.getElementById('search-field').focus();
    };
}


// Search is triggered by search key
async function trigSearch(e) {
    if (e.code == "Space" && e.shiftKey) {
        toggleSearch();
    };
}

async function setTitle(elemName, val) {
    let oldVal, elem;
    elem = document.getElementById(elemName);
    elem.innerHTML = val + elem.innerHTML;
}

async function setDisplayVars() {
    let qLS, qLC, qLT, qLIC, setName, linkName, quicklink;
    setTitle("search-title", display["searchTitle"]);
    setTitle("go", display["searchTerm"]);
    qLC = document.getElementById("quicklink-container");
    for (setName in display["quicklinkSet"]) {
        qLS = document.createElement('div');
        qLS.setAttribute('class', 'quicklink-set');
        qLT = document.createElement('div');
        qLT.setAttribute('class', 'quicklink-title');
        qLT.innerHTML = setName;
        qLS.appendChild(qLT);
        qLIC = document.createElement('div');
        qLIC.setAttribute('class', 'quicklink-internal-container');
        for (linkName in display["quicklinkSet"][setName]) {
            quicklink = document.createElement('a');
            quicklink.setAttribute('class', 'quicklink');
            quicklink.setAttribute(
                'href', display["quicklinkSet"][setName][linkName]
            );
            quicklink.setAttribute('target', '_blank');
            quicklink.innerHTML = linkName;
            qLIC.appendChild(quicklink);
        };
        qLS.appendChild(qLIC);
        qLC.appendChild(qLS);
    };
}

// def main()
window.onload = () => {
    setDisplayVars();
    document.addEventListener('keydown', trigSearch);
    document.getElementById("search-field").addEventListener(
        'keydown', function (e) {
            if (e.code == "Enter") {
                callSearx();
            }
        }
    );
    setCityWeather(display["places"]);
    initClock();
    setTime();
    setInterval( () => {
        setCityWeather(display["places"]);
    }, 15 * 60 * 1000);
    setInterval(setTime, 1 * 1000);
};

