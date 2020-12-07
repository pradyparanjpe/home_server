// -*- coding: utf-8; mode: javascript; -*-
// Copyright 2020 Pradyumna Paranjape
// This file is part of home_server.
//
// home_server is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// home_server is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with home_server.  If not, see <https://www.gnu.org/licenses/>.
//

var Item, itemIdx;

// item structure:
// content: '', status: false, username: Nobody, date: Null

if ( typeof username === 'undefined' ) {
    var username = 'Nobody';
}

if ( typeof todoDB === 'undefined' ) {
    var todoDB = [];
}

if ( typeof admin === 'undefined') {
    var admin = 0;
}

function getRank(child) {
    let child_index = 0;
    let tempChild = child;
    while ((tempChild = tempChild.previousSibling) != null){
        child_index++;
    }
    return child_index;
}

async function pushDown(Item) {
    let pos = getRank(Item);
    if (pos == todoDB.length-1){
        return;
    }
    let data = todoDB[pos];
    todoDB.splice(pos, 1);
    todoDB.splice(pos+1, 0, data);
    updateList();
}


async function pushUp(Item) {
    let pos = getRank(Item);
    if (pos == 0){
        return;
    }
    let data = todoDB[pos];
    todoDB.splice(pos, 1);
    todoDB.splice(pos-1, 0, data);
    updateList();
}


async function delItem(Item) {
    todoDB.splice(getRank(Item), 1);
    // todoDB.splice(getRank(this.parentElement), 1);
    updateList();
}


async function doneItem(Item) {
    let idx = getRank(Item);
    todoDB[idx]['status'] ^= 1;
    todoDB[idx]['username'] = username;
    todoDB[idx]['date'] = null;
    updateList();
}


async function addItem() {
    let inputValue = document.getElementById("text-input").value;
    document.getElementById("text-input").value = '';
    // 'blank' must have been unintentional
    if (inputValue == '') {
        return;
    }
    todoDB.push({content: inputValue, status: 0,
                 username: username, date: null});
    updateList();
}


async function deList() {
    // clear fields
    let listDisp = document.getElementById("todoList");
    while (listDisp.firstChild) {
        listDisp.removeChild(listDisp.firstChild);
    }
}


// create <done>, <move up>, <move down>, <delete> buttons
function addKeys(Item, owner=0) {
    let orgKeys = [
        ["\u2714", () => doneItem(Item)],
        ["\u25B2", () => pushUp(Item)],
        ["\u25Bc", () => pushDown(Item)],
    ];
    let orgDiv = document.createElement("DIV");
    orgDiv.className = 'org-keys';
    orgKeys.forEach(k => {
        let span = document.createElement("SPAN");
        span.innerHTML = k[0];
        span.className = 'org-btn';
        span.onclick = k[1];
        orgDiv.appendChild(span);
    });
    // . Button is active only with priviliges
    let span = document.createElement("SPAN");
    if ((owner + admin) > 0) {
        // Privileged
        span.innerHTML = "\u00D7";  // cross
        span.className = 'org-btn';
        span.onclick = () => delItem(Item);  // bind to deletion
    }
    orgDiv.appendChild(span);
    return orgDiv;
}


function qualify(todo){
    let qual = document.createElement("DIV");
    qual.className = "qual-text";
    let uname = document.createElement('TEXT');
    let timestamp = document.createElement('TEXT');
    uname.innerHTML = " by " + todo['username'] + " ";
    if (todo['date'] !== null ) {
        timestamp.innerHTML = " on " + todo['date'];
    } else {
        timestamp.innerHTML = " just now ";
    }

    qual.appendChild(uname);
    qual.appendChild(timestamp);
    return qual;
}


function wordtext(todo) {
    let texts = document.createElement("DIV");
    texts.className = "texts";
    let maindiv = document.createElement("DIV");
    maindiv.className = 'main-item';
    let maintxt = document.createElement("TEXT");
    maintxt.innerHTML = todo['content'];
    maindiv.appendChild(maintxt);
    texts.appendChild(maindiv);
    texts.appendChild(qualify(todo));
    return texts;
}


function reList() {
    todoDB.forEach(todo => {
        let owner = 0;
        if ( username == todo['username']) {
            owner = 1;
        }
        let liItem = document.createElement("li");
        if (todo['status']) {
            liItem.classList.toggle('checked');
        }
        let text = wordtext(todo);
        liItem.appendChild(text);
        if ((owner + admin) > 0) {
            text.onclick = () => editItem(liItem); // click binding
        }
        liItem.appendChild(addKeys(liItem, owner=owner));
        document.getElementById('todoList').appendChild(liItem);
    });
}


function updateList() {
    deList();
    reList();
}


async function editItem(Item) {
    itemIdx = getRank(Item);
    if (document.getElementById("edit-input") != null) {
        // save _that_ field
        upDB(itemIdx);
    }
    // Item = text.parentElement;

    // disable listener
    Item.onclick = () => false;

    let editField = document.createElement('input');
    let editButton = document.createElement('span');

    // A temporary Edit field
    editField.type = 'text';
    editField.id = 'edit-input';
    editField.value = todoDB[itemIdx]['content'];
    editButton.className = 'addbtn';
    editButton.onclick = () => upDB(itemIdx);
    editButton.innerHTML = 'Update';
    // Clear current list field
    while (Item.firstChild) {
        await Item.removeChild(Item.firstChild);
    }

    // Place Edit field in its stead
    await Item.appendChild(editField);
    Item.appendChild(editButton);

    // Listen on enter return
    document.getElementById("edit-input").addEventListener(
        'keydown', function (e) {
            if (e.code == "Enter") {
                upDB(itemIdx);
            }
        }
    );
}


async function upDB(itemIdx) {
    let inputValue = document.getElementById("edit-input").value;

    // 'Blank' must have been unintentional
    if (inputValue != '') {
        todoDB[itemIdx]['content'] = inputValue;
        if (admin === 0) {
            todoDB[itemIdx]['username'] = username;
        }
        todoDB[itemIdx]['date'] = null;
    }
    updateList();
}


async function fieldListen() {
    // Global Listener listens on for enter on addItem
    document.getElementById("text-input").addEventListener(
        'keydown', function (e) {
            if (e.code == "Enter") {
                addItem();
            }
        }
    );
}


async function reload() {
    location.reload();
}


async function save() {
    if (todoDB.length == 0){
        console.log("todoDB, " + todoDB + ", is an empty array empty");
        return;
    }
    // Creating a XHR object
    let xhr = new XMLHttpRequest();
    let url = "todo";

    // open a connection
    xhr.open("POST", url, true);
    // Set the request header i.e. which type of content you are sending
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
        if (this.status >= 200 && this.status < 300) {
            console.log(xhr.response);
            window.location = xhr.response;
        } else {
            console.log({
                status: this.status,
                statusText: xhr.statusText
            });
        }
    };
    xhr.onerror = function () {
        console.log({
            status: this.status,
            statusText: xhr.statusText
        });
    };
    xhr.send(JSON.stringify(todoDB));
}


window.onload = () => {
    updateList();
    fieldListen();
};

