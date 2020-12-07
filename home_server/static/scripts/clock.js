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

const TAU = Math.PI * 2;
var date = new Date;
var n_hrs = 12;
var span = document.getElementById('dial').height/2;
var faceCol = "#3fff9f";

async function setDial() {
    let canvas = document.getElementById('dial');
    let ctx = canvas.getContext('2d');
    await ctx.clearRect(0, 0, canvas.width, canvas.height);
    axisfulc();
    // sTicks();
    hTicks();

    async function axisfulc() {
        await ctx.beginPath();
        ctx.lineWidth = 3;
        ctx.strokeStyle = faceCol;
        ctx.arc(canvas.width / 2, canvas.height / 2, 2, 0, TAU);
        ctx.stroke();
    }

    async function hTicks() {
        for (let i = 0; i < n_hrs; i++) {
            let angle = (i - 3) * TAU / n_hrs;
            let x1 = (canvas.width / 2) + Math.cos(angle) * span * 0.9;
            let y1 = (canvas.height / 2) + Math.sin(angle) * span * 0.9;
            let x2 = (canvas.width / 2) + Math.cos(angle) * span * 0.85;
            let y2 = (canvas.height / 2) + Math.sin(angle) * span * 0.85;
            await ctx.beginPath();
            ctx.lineWidth = ((!(angle % (TAU/4))) ? 4 : 1 );
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = faceCol;
            ctx.stroke();
        }
    }

    async function sTicks() {
        for (let i = 0; i < 60; i++) {
            let angle = (i - 3) * TAU / 60;
            let x1 = (canvas.width / 2) + Math.cos(angle) * span * 0.9;
            let y1 = (canvas.height / 2) + Math.sin(angle) * span * 0.9;
            let x2 = (canvas.width / 2) + Math.cos(angle)  * span * 0.99;
            let y2 = (canvas.height / 2) + Math.sin(angle) * span * 0.99;
            await ctx.beginPath();
            ctx.lineWidth = 1;
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = faceCol;
            ctx.stroke();
        }
    }
}


async function pointHand(canvas, angle, lineWidth, lengthSpan, tail=false) {
    let ctx = canvas.getContext('2d');
    await ctx.beginPath();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = lineWidth;
    if (tail) {
        ctx.moveTo((canvas.width / 2 - Math.cos(angle)
                    * span * lengthSpan * 0.3),
                   canvas.height / 2 - Math.sin(angle)
                   * span * lengthSpan * 0.3);
    } else {
        ctx.moveTo(canvas.width / 2, canvas.height / 2);  // Centre
    };
    ctx.lineTo((canvas.width / 2 + Math.cos(angle) * span * lengthSpan),
               canvas.height / 2 + Math.sin(angle) * span * lengthSpan);
    ctx.strokeStyle = faceCol;
    ctx.stroke();
}


async function pointHandHrs() {
    let canvas = document.getElementById('hHrs');
    let angle = TAU * ( date.getHours()/n_hrs  // coarse
                        + date.getMinutes()/(n_hrs * 60)  // fine
                        + (n_hrs - 18)/24 );  // zero-offset
    pointHand(canvas, angle, 5, 0.6);
}

async function pointHandMin() {
    let canvas = document.getElementById('hMin');
    let angle = TAU * (date.getMinutes()/60  // coarse
                       + date.getSeconds()/3600  // fine
                       - 0.25);  // offset
    if (!((angle + 0.25 * TAU) % (TAU/6)))
        pointHandHrs();
    pointHand(canvas, angle, 3, 0.8);
}

async function pointHandSec() {
    let canvas = document.getElementById('hSec');
    let angle = TAU * (date.getSeconds()/60  // coarse
                       - 0.25) ;  // offset
    if (!((angle + 0.25 * TAU) % (TAU/6)))
        pointHandMin();
    pointHand(canvas, angle, 1, 0.7, true);
}

async function initClock() {
    setDial();
    pointHandHrs();
    pointHandMin();
    pointHandSec();
}

async function switch_hrs() {
    n_hrs = ((n_hrs==12) ? 24 : 12);
    initClock();
}

// Show Time
async function setTime() {
    date = new Date;
    let min = date.getMinutes(),
        sec = date.getSeconds(),
        hour = date.getHours() % n_hrs;
    hour = (!(hour)) ? date.getHours() : hour;
    pointHandSec();
    let timeStr = await "" +
        (hour < 10 ? ("0" + hour) : hour) + " : " +
        (min < 10 ? ("0" + min) : min) + " : " +
        (sec < 10 ? ("0" + sec) : sec);
    document.getElementById('digital-clock').innerHTML = timeStr;
}

