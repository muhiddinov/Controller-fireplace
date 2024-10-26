var kvolume = 15, kcooler = 0, kbrightness = 50;

function workSwitch(e) {
  var switchButton = document.getElementById("power");
  var checkButton = false;
  if (switchButton.checked) {
    checkButton = true
    console.log("On!");
  } else {
    console.log("Off!");
  }
  fetch('/work?' + new URLSearchParams({value: checkButton}).toString()).then( response => { console.log(response); } )
}
function coolerInc(e) {
    kcooler = kcooler + 1;
    if (kcooler > 6) kcooler = 0;
    console.log(kcooler);
    fetch('/cooler?' + new URLSearchParams({value: kcooler}).toString()).then( response => { console.log(response); } )
}
function soundDecr(e) {
    if (kvolume > 0) {
        kvolume = kvolume - 1;
    }
    console.log(kvolume);
    fetch('/volume?' + new URLSearchParams({value: kvolume}).toString()).then( response => { console.log(response); } )
}
function soundInc(e) {
    if (kvolume < 30) {
        kvolume = kvolume + 1;
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
        kbrightness = kbrightness + 10;
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