const favLnk = document.getElementById("favicon-link");

const dark = window.matchMedia("(prefers-color-scheme: dark)");

const titIm0 = document.getElementById("title-image0");
const titIm1 = document.getElementById("title-image1");

const lightButton = document.getElementById("light-button");
const  autoButton = document.getElementById( "auto-button");
const  darkButton = document.getElementById( "dark-button");

var defaultIcons = [...document.getElementsByClassName("default-icon")];


lightButton.addEventListener("click", changeTheme);
autoButton.addEventListener("click", changeTheme);
darkButton.addEventListener("click", changeTheme);

var mode;


function detectTheme() {
    var cookieTheme = getCookie("theme");
    
    if(cookieTheme === "dark") {
        mode = "dark";
        
        document.documentElement.style.setProperty("color-scheme", "dark");
        
        darkButton.style.setProperty("background-color",
                                     "light-dark(#686070, #706068)");
    } else if(cookieTheme === "light") {
        mode = "light";
        
        document.documentElement.style.setProperty("color-scheme", "light");
        
        lightButton.style.setProperty("background-color",
                                      "light-dark(#686070, #706068)");
    } else {
        mode = "auto";
        
        document.documentElement.style.removeProperty("color-scheme");
        
        autoButton.style.setProperty("background-color",
                                     "light-dark(#686070, #706068)");
    }
};


function updateTheme() {
    defaultIcons = [...document.getElementsByClassName("default-icon")];
    
    if(mode == "dark" || (mode == "auto" && dark.matches)) {
        //favLnk.href = "/images/emu-logo-white.png";
        //titIm0.src = "/images/emu-logo-light.png";
        //titIm1.src = "/images/emu-logo-light.png";
        
        for(var i = 0; i < defaultIcons.length; i++) {
            defaultIcons[i].src = "/images/default-white.png";
        }
    } else {
        //favLnk.href = "/images/emu-logo-black.png";
        //titIm0.src = "/images/emu-logo-dark.png";
        //titIm1.src = "/images/emu-logo-dark.png";
        
        for(var i = 0; i < defaultIcons.length; i++) {
            defaultIcons[i].src = "/images/default-black.png";
        }
    }
};


function changeTheme(event) {
    const  darkChild = [ darkButton, ...getDescendants( darkButton)];
    const  autoChild = [ autoButton, ...getDescendants( autoButton)];
    const lightChild = [lightButton, ...getDescendants(lightButton)];
    
    darkButton.style.removeProperty("background-color");
    autoButton.style.removeProperty("background-color");
    lightButton.style.removeProperty("background-color");
    
    if(darkChild.includes(event.target)) {
        mode = "dark";
        
        document.documentElement.style.setProperty("color-scheme", "dark");
        
        darkButton.style.setProperty("background-color",
                                     "light-dark(#686070, #706068)");
        
        setCookie("theme", "dark");
    } else if(lightChild.includes(event.target)) {
        mode = "light";
        
        document.documentElement.style.setProperty("color-scheme", "light");
        
        lightButton.style.setProperty("background-color",
                                      "light-dark(#686070, #706068)");
        
        setCookie("theme", "light");
    } else if(autoChild.includes(event.target)) {
        mode = "auto";
        
        document.documentElement.style.removeProperty("color-scheme");
        
        autoButton.style.setProperty("background-color",
                                     "light-dark(#686070, #706068)");
        
        delCookie("theme");
    }
    
    updateTheme();
};

detectTheme();
updateTheme();

setInterval(updateTheme, 500);
