const displayBox = document.getElementById("display-box");
const displayImg = document.getElementById("display-image");
const displayTtl = document.getElementById("display-title");
const displayTxt = document.getElementById("display-text");

const displayClose = document.getElementById("display-close");
const displayLeft  = document.getElementById("display-left");
const displayRight = document.getElementById("display-right");

const grids = document.getElementsByClassName("page-grid");

gridBoxes = [];

for(var i = 0; i < grids.length; i++) {
    gridBoxes.push(grids[i].getElementsByClassName("inner-box"));
}

const setGridActions = () => {
    for(var i = 0; i < gridBoxes.length; i++) {
        for(var j = 0; j < gridBoxes[i].length; j++) {
            gridBoxes[i][j].addEventListener("click", gridClick);
        }
    }
    
    document.addEventListener("click", closeDisplay);
    
    displayLeft.addEventListener("click", previousDisplay);
    displayRight.addEventListener("click", nextDisplay);
};


//var displayGrid = gridBoxes;
var displayGrid = -1;
var displayElement = -1;


function gridClick(event) {
    displayGrid = -1
    displayElement = -1
    
    for(var i = 0; i < gridBoxes.length; i++) {
        displayElement = [...gridBoxes[i]].indexOf(event.currentTarget);
        
        if(displayElement == -1) {
            continue;
        } else {
            displayGrid = i;
            
            break;
        }
    }
    
    if(setDisplay(gridBoxes[displayGrid], displayElement)) {
        displayBox.style.display = "block";
    }
};


function setDisplay(set, idx) {
    if(idx != -1) {
        var img = set[idx].getElementsByTagName("img")[0];
        var ttl = set[idx].getElementsByClassName("grid-text")[0];
        var txt = set[idx].getElementsByClassName("grid-display-text")[0];
        
        if(typeof img !== "undefined" && img !== null) {
            displayImg.src = img.src;
            displayImg.alt = img.src.split('/')[img.src.split('/').length - 1];
            
            if(img.classList.contains("default-icon")) {
                displayImg.classList.add("default-icon");
            } else {
                displayImg.classList.remove("default-icon");
            }
        } else {
            displayImg.src = "";
            displayImg.alt = "T&mu;";
        }
        
        if(typeof ttl !== "undefined" && ttl !== null) {
            displayTtl.innerHTML = ttl.innerHTML;
        } else {
            displayTtl.innerHTML = "";
        }
        
        if(typeof txt !== "undefined" && txt !== null) {
            displayTxt.innerHTML = txt.innerHTML;
        } else {
            displayTxt.innerHTML = "";
        }
        
        //console.log(displayTtl.innerText);
        
        return true;
    }
    
    return false;
};


function nextDisplay(event) {
    if(displayElement != -1) {
        displayElement++;
        
        if(displayElement == gridBoxes[displayGrid].length) {
            displayElement = 0;
        }
        
        setDisplay(gridBoxes[displayGrid], displayElement);
    }
};


function previousDisplay(event) {
    if(displayElement != -1) {
        displayElement--;
        
        if(displayElement == -1) {
            displayElement = gridBoxes[displayGrid].length - 1;
        }
        
        setDisplay(gridBoxes[displayGrid], displayElement);
    }
};


function closeDisplay(event) {
    const closeChild = [displayClose, ...getDescendants(displayClose)];
    const displChild = [displayBox,   ...getDescendants(displayBox)];
    
    var gridChild = [];
    
    for(var i = 0; i < gridBoxes.length; i++) {
        for(var j = 0; j < gridBoxes[i].length; j++) {
            gridChild = [...gridChild, gridBoxes[i][j],
                         ...getDescendants(gridBoxes[i][j])];
        }
    }
    
    if(closeChild.includes(event.target)
    || !(displChild.includes(event.target)
      || gridChild.includes(event.target))) {
        displayBox.style.display = "none";
        
        displayElement = -1;
    }
};


setGridActions();
