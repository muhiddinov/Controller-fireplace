function coolerSwitch(e) {
  var switchButton = document.getElementById("cooler");
  
  var toggleValue = "";
  if (switchButton.checked) {
    console.log("On!");
    toggleValue = "Cooler ON";
  } else {
    console.log("Off!");
    toggleValue = "Cooler OFF"
  }
  fetch( `/toggleCooler`)
  .then( response => {
    console.log(response);
  } )
}

function workSwitch(e) {
  var switchButton = document.getElementById("power");
  
  var toggleValue = "";
  if (switchButton.checked) {
    console.log("On!");
    toggleValue = "ON";
  } else {
    console.log("Off!");
    toggleValue = "OFF"
  }
  fetch( '/togglePower')
  .then( response => {
    console.log(response);
  } )
}

function soundDecr(e) {
    var pVol = parseInt(document.getElementById("volume").innerHTML, 10);
    if (pVol > 0) {
        pVol = pVol - 10;
    }
    document.getElementById("volume").innerHTML = pVol;
    console.log(pVol);
    
    fetch('/volume?' + new URLSearchParams({value: pVol}).toString()).then( response => { console.log(response); } )
}

function soundInc(e) {
    var pVol = parseInt(document.getElementById("volume").innerHTML, 10);
    if (pVol < 100) {
        pVol = pVol + 10;
    }
    document.getElementById("volume").innerHTML = pVol;
    console.log(pVol);
    
    fetch('/volume?' + new URLSearchParams({value: pVol}).toString()).then( response => { console.log(response); } )
}

function brightDecr(e) {
    var pVol = parseInt(document.getElementById("brightness").innerHTML, 10);
    if (pVol > 0) {
        pVol = pVol - 10;
    }
    document.getElementById("brightness").innerHTML = pVol;
    console.log(pVol);
    
    fetch('/brigtness?' + new URLSearchParams({value: pVol}).toString()).then( response => { console.log(response); } )
}

function brightInc(e) {
    var pVol = parseInt(document.getElementById("brightness").innerHTML, 10);
    if (pVol < 100) {
        pVol = pVol + 10;
    }
    document.getElementById("brightness").innerHTML = pVol;
    console.log(pVol);
    
    fetch('/brigtness?' + new URLSearchParams({value: pVol}).toString()).then( response => { console.log(response); } )
}

function yellow(e) {
    fetch('/yellow').then( response => { console.log(response); } )
}

function blue(e) {
    fetch('/blue').then( response => { console.log(response); } )
}

function red(e) {
    fetch('/red').then( response => { console.log(response); } )
}

function orange(e) {
    fetch('/orange').then( response => { console.log(response); } )
}

function green(e) {
    fetch('/green').then( response => { console.log(response); } )
}