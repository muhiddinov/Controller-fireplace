var kvolume = 0, kcooler = 0, kbrightness = 0;

function workSwitch(e) {
  var switchButton = document.getElementById("power");
  if (switchButton.checked) {
    console.log("On!");
  } else {
    console.log("Off!");
  }
  fetch( '/togglePower')
  .then( response => {
    console.log(response);
  } )
}
function coolerInc(e) {
    kcooler = kcooler + 1;
    if (kcooler > 6) kcooler = 0;
    console.log(kcooler);
    fetch('/cooler?' + new URLSearchParams({value: kcooler}).toString()).then( response => { console.log(response); } )
}
function soundDecr(e) {
    if (kvolume > 0) {
        kvolume = kvolume - 10;
    }
    console.log(kvolume);
    fetch('/volume?' + new URLSearchParams({value: kvolume}).toString()).then( response => { console.log(response); } )
}
function soundInc(e) {
    var pVol = parseInt(document.getElementById("volume").innerHTML, 10);
    if (kvolume < 100) {
        kvolume = kvolume + 10;
    }
    console.log(kvolume);
    fetch('/volume?' + new URLSearchParams({value: kvolume}).toString()).then( response => { console.log(response); } )
}
function brightDecr(e) {
    if (kbrightness > 0) {
        kbrightness = kbrightness - 10;
    }
    console.log(kbrightness);
    fetch('/brigtness?' + new URLSearchParams({value: kbrightness}).toString()).then( response => { console.log(response); } )
}

function brightInc(e) {
    if (kbrightness < 100) {
        kbrightness = pVkbrightnessol + 10;
    }
    console.log(kbrightness);
    fetch('/brigtness?' + new URLSearchParams({value: kbrightness}).toString()).then( response => { console.log(response); } )
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