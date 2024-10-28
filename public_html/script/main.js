function toggleVisible(element) {
    if(element.style.display === "block") {
        element.style.display = "none";
    } else {
        element.style.display = "block";
    }
};


function stopProp(event) {
    event.stopPropagation();
};


function getDescendants(elem, all = []) {
    all.push(...elem.childNodes);
    
    for (const child of elem.childNodes) {
        getDescendants(child, all);
    }
    
    return all;
};


function setCookie(name, value, maxAge, path) {
    var keyVal  = name + '=' + value + ';';
    var domain  = "";
    var pathStr = "Path=/;";
  //var expires = "Max-Age=31557600000;"; // 1000 years with the 4 year rule
    var expires = "Max-Age=31556952000;"; // 1000 years with the 100, 400 rule
    var secure  = "Secure;";
    var site    = "SameSite=Strict;"
    
    if(path !== undefined && path !== null) {
        pathStr = "Path=" + path + ';';
    } else {
        path = "/";
    }
    
    if(maxAge !== undefined && maxAge !== null) {
        expires = "Max-Age=" + maxAge + ';';
    }
    
    document.cookie = keyVal + domain + pathStr + expires + secure + site;
};


function getCookie(name) {
    for(cookie of document.cookie.split(';')) {
        while(cookie[0] == ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        
        if(cookie.indexOf(name + '=') == 0) {
            return cookie.substring(name.length + 1, cookie.length);
        }
    }
    
    return null;
};


function delCookie(name, path) {
    if(path === undefined || path === null) {
        path = "/";
    }
    
    document.cookie = name + "=;path=" + path + ";Max-Age=0;SameSite=Strict;";
};
