/*
    MIT License

    Copyright (c) 2018 ShellAddicted <github.com/ShellAddicted>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
*/

wsCameraConn = null;

class wsCamera{
    constructor(serverURL, imgID) {
        this._serverURL = serverURL;
        this._nd = document.getElementById(imgID);
    }

    start(){
        this._conn = new WebSocket(this._serverURL);
        this._conn.onmessage = (msg) => {
            window.URL.revokeObjectURL(this._nd.src);
            this._nd.src = window.URL.createObjectURL(msg.data);
        }
    }

    stop(){
        this._conn.close();
        this._conn = null;
        this._nd.src="#"
    }
}