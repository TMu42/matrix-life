const user = document.getElementById("usr");
const home = document.getElementById("home");
const feat = document.getElementById("featured");
const actv = document.getElementById("active");
const futr = document.getElementById("future");
const hmbg = document.getElementById("hamburger");
const menu = document.getElementById("menu-bar");
const drop = document.getElementById("hamburger-drop-menu");
const body = document.getElementById("body");

const setMenuActions = () => {
    user.addEventListener("click", linkButton);
    home.addEventListener("click", linkButton);
    feat.addEventListener("click", linkButton);
    actv.addEventListener("click", linkButton);
    futr.addEventListener("click", linkButton);
    
    drop.addEventListener("click", stopProp);
    
    document.addEventListener("click", toggleHamburger);
};


var hamburger = false;


function linkButton(event) {
    const buttonId = event.currentTarget.id;
    
    if(buttonId === "usr") {
        location.href = "https://github.com/TMu42";
    } else if(buttonId === "home") {
        location.href = "/";
    } else if(buttonId === "featured") {
        location.href = "/#Featured Projects";
    } else if(buttonId === "active") {
        location.href = "/#Active Projects";
    } else if(buttonId === "future") {
        location.href = "/#Future Projects";
    }
};


function toggleHamburger(event) {
    const burgerChild = [hmbg, ...getDescendants(hmbg)];
    const dropChild   = [drop, ...getDescendants(drop)];
    
    if(burgerChild.includes(event.target)) {
        if(hamburger) {
            hideHamburger(event);
        } else {
            showHamburger(event);
        }
    } else if(!dropChild.includes(event.target)) {
        hideHamburger(event);
    }
};


function hideHamburger(event) {
    drop.style.display = "none";
    
    hmbg.innerHTML = '&#x2630;&#xFE0E;'; /*'☰'*/
    
    hamburger = false;
};


function showHamburger(event) {
    drop.style.display = "block";
    
    hmbg.innerHTML = 'x';
    
    hamburger = true;
};


setMenuActions();
