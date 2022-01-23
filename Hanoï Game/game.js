let startForm = document.getElementsByClassName('startForm');
let gameArea = document.getElementById('gameArea');
let endText = document.getElementById('endText');
let pseudo;
let level;
let title = document.getElementById('Title');
let towersElts = document.getElementsByClassName('tower');
let towerSize;
let firstTower = new Array();
let secondTower = new Array();
let thirdTower = new Array();
let transitorElt = null;
let startTower = null;
let endTower = null;
let counter = 0;
let counterDiv;

function Start() {
    pseudo = document.getElementById('Pseudo').value;
    level = document.getElementById('Level').value;
    level = parseInt(level);
    document.getElementById('Pseudo').value = "";
    document.getElementById('Level').value = "";
    for (elt of startForm){elt.classList.add('noreveal');}
    title.style.position="fixed";
    title.style.width="100%";
    title.style.textAlign="center";
    title.style.top="2rem";
    gameArea.classList.remove('noreveal');
    game=createGame(level);
    play();
}

function play() {
    if(!isWinned()){
        if (firstTower.length!=0){
            addEvent(firstTower[firstTower.length - 1],"click", firstTowerTransitor);
        }
        if (secondTower.length!=0){
            addEvent(secondTower[secondTower.length - 1],"click", secondTowerTransitor);
        }
        if (thirdTower.length!=0){
            addEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerTransitor);
        }
    }else{
        document.getElementById("endCounter").innerHTML=counter;
        gameArea.classList.add('noreveal');
        endText.classList.remove('noreveal');
    }
}

function createGame(level) {
    towerSize = level*2+2;
    for (elt of towersElts) {
        elt.style.height= towerSize+"rem";
        elt.style.bottom= 'calc(50% - '+towerSize/2+"rem)";
    }
    for(let i=level; i>0; i--) {
        let elt=document.createElement("div");
        gameArea.appendChild(elt);
        elt.id= "Block"+i;
        elt.classList.add("Block");
        elt.style.width= i+"rem";
        elt.style.height="2rem";
        elt.innerHTML=i;
        elt.style.position= "fixed";
        elt.style.left="calc(25% - "+i/2+"rem)";
        elt.style.bottom= 'calc(50% - '+towerSize/2+"rem + 1rem + "+(level-i)*2+"rem)";
        elt.style.backgroundColor= 'rgb('+(150/level)*(level+1-i)+','+245+','+255+')';
        firstTower.push(elt);
    }
    counterDiv=document.createElement("div");
    gameArea.appendChild(counterDiv);
    counterDiv.innerHTML="Move Count: "+counter;
    counterDiv.style.position="fixed";
    counterDiv.style.top="3rem";
    counterDiv.style.left="80%";
}

function round() {
    if (moveIsPermitted(transitorElt, endTower)) {
        startTower.pop();
        endTower.push(transitorElt);
        towerRefresh();
        transitorElt.style.transform="scale(1)";
        transitorElt.style.zIndex= "auto";
        transitorElt=null;
        startTower=null;
        endTower=null;
        counter++;
        counterDiv.innerHTML="Move Count: "+counter;
        play();
    }else{
        towerRefresh();
        transitorElt.style.transform="scale(1)";
        transitorElt.style.zIndex= "auto";
        transitorElt=null;
        startTower=null;
        endTower=null;
        play();
    }
}

function towerRefresh() {
    for (let i1=0;i1<firstTower.length;i1++){
        firstTower[i1].style.left="calc(25% - "+parseInt(firstTower[i1].style.width)/2+"rem)";
        firstTower[i1].style.bottom='calc(50% - '+towerSize/2+"rem + 1rem + "+i1*2+"rem)";
    }
    for (let i2=0;i2<secondTower.length;i2++){
        secondTower[i2].style.left="calc(50% - "+parseInt(secondTower[i2].style.width)/2+"rem)";
        secondTower[i2].style.bottom='calc(50% - '+towerSize/2+"rem + 1rem + "+i2*2+"rem)";
    }
    for (let i3=0;i3<thirdTower.length;i3++){
        thirdTower[i3].style.left="calc(75% - "+parseInt(thirdTower[i3].style.width)/2+"rem)";
        thirdTower[i3].style.bottom='calc(50% - '+towerSize/2+"rem + 1rem + "+i3*2+"rem)";
    }
}

function moveIsPermitted(blockMoved, arrivalTower) {
    if(transitorElt==null || arrivalTower==null){
        return false;
    }else if (arrivalTower.length==0){
        return true;
    }else{
        return !(parseInt(blockMoved.style.width) > parseInt(arrivalTower[arrivalTower.length - 1].style.width));
    }
}

function isWinned() {
    return (firstTower.length==0 && secondTower.length==0);
}

function firstTowerTransitor() {
    transitorElt=firstTower[firstTower.length-1];
    transitorElt.style.transform="scale(1.25)";
    transitorElt.style.zIndex= "100";
    addEvent(document,'mousemove',mousePos);
    startTower=firstTower;
    delEvent(firstTower[firstTower.length - 1],"click", firstTowerTransitor);
    if (secondTower.length!=0){
        delEvent(secondTower[secondTower.length - 1],"click", secondTowerTransitor);
    }
    if (thirdTower.length!=0){
        delEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerTransitor);
    }
    addEvent(document.getElementById("firstTower"),"click", firstTowerArrival);
    addEvent(document.getElementById("secondTower"),"click", secondTowerArrival);
    addEvent(document.getElementById("thirdTower"),"click", thirdTowerArrival);
    if (firstTower.length>1){
        addEvent(firstTower[firstTower.length - 2],"click", firstTowerArrival);
    }
    if (secondTower.length!=0){
        addEvent(secondTower[secondTower.length - 1],"click", secondTowerArrival);
    }
    if (thirdTower.length!=0){
        addEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerArrival);
    }
    
    
}
function secondTowerTransitor() {
    transitorElt=secondTower[secondTower.length-1];
    transitorElt.style.transform="scale(1.25)";
    transitorElt.style.zIndex= "100";
    addEvent(document,'mousemove',mousePos);
    startTower=secondTower;
    if (firstTower.length!=0){
        delEvent(firstTower[firstTower.length - 1],"click", firstTowerTransitor);
    }
    delEvent(secondTower[secondTower.length - 1],"click", secondTowerTransitor);
    if (thirdTower.length!=0){
        delEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerTransitor);
    }

    addEvent(document.getElementById("firstTower"),"click", firstTowerArrival);
    addEvent(document.getElementById("secondTower"),"click", secondTowerArrival);
    addEvent(document.getElementById("thirdTower"),"click", thirdTowerArrival);
    if (firstTower.length!=0){
        addEvent(firstTower[firstTower.length - 1],"click", firstTowerArrival);
    }
    if (secondTower.length>1){
        addEvent(secondTower[secondTower.length - 2],"click", secondTowerArrival);
    }
    if (thirdTower.length!=0){
        addEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerArrival);
    }
}
function thirdTowerTransitor() {
    transitorElt=thirdTower[thirdTower.length-1];
    transitorElt.style.transform="scale(1.25)";
    transitorElt.style.zIndex= "100";
    addEvent(document,'mousemove',mousePos);
    startTower=thirdTower;
    if (firstTower.length!=0){
        delEvent(firstTower[firstTower.length - 1],"click", firstTowerTransitor);
    }
    if (secondTower.length!=0){
        delEvent(secondTower[secondTower.length - 1],"click", secondTowerTransitor);
    }
    delEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerTransitor);

    addEvent(document.getElementById("firstTower"),"click", firstTowerArrival);
    addEvent(document.getElementById("secondTower"),"click", secondTowerArrival);
    addEvent(document.getElementById("thirdTower"),"click", thirdTowerArrival);
    if (firstTower.length!=0){
        addEvent(firstTower[firstTower.length - 1],"click", firstTowerArrival);
    }
    if (secondTower.length!=0){
        addEvent(secondTower[secondTower.length - 1],"click", secondTowerArrival);
    }
    if (thirdTower.length>1){
        addEvent(thirdTower[thirdTower.length - 2],"click", thirdTowerArrival);
    }
}

function firstTowerArrival() {
    endTower=firstTower;
    delEvent(document,'mousemove',mousePos);

    delEvent(document.getElementById("firstTower"),"click", firstTowerArrival);
    delEvent(document.getElementById("secondTower"),"click", secondTowerArrival);
    delEvent(document.getElementById("thirdTower"),"click", thirdTowerArrival);
    if(firstTower.length!=0){
        delEvent(firstTower[firstTower.length - 1],"click", firstTowerArrival);
    }
    if(secondTower.length!=0){
        delEvent(secondTower[secondTower.length - 1],"click", secondTowerArrival);
    }
    if(thirdTower.length!=0){
        delEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerArrival);
    }

    round();
}
function secondTowerArrival() {
    endTower=secondTower;
    delEvent(document,'mousemove',mousePos);

    delEvent(document.getElementById("firstTower"),"click", firstTowerArrival);
    delEvent(document.getElementById("secondTower"),"click", secondTowerArrival);
    delEvent(document.getElementById("thirdTower"),"click", thirdTowerArrival);
    if(firstTower.length!=0){
        delEvent(firstTower[firstTower.length - 1],"click", firstTowerArrival);
    }
    if(secondTower.length!=0){
        delEvent(secondTower[secondTower.length - 1],"click", secondTowerArrival);
    }
    if(thirdTower.length!=0){
        delEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerArrival);
    }

    round();
}
function thirdTowerArrival() {
    endTower=thirdTower;
    delEvent(document,'mousemove',mousePos);

    delEvent(document.getElementById("firstTower"),"click", firstTowerArrival);
    delEvent(document.getElementById("secondTower"),"click", secondTowerArrival);
    delEvent(document.getElementById("thirdTower"),"click", thirdTowerArrival);
    if(firstTower.length!=0){
        delEvent(firstTower[firstTower.length - 1],"click", firstTowerArrival);
    }
    if(secondTower.length!=0){
        delEvent(secondTower[secondTower.length - 1],"click", secondTowerArrival);
    }
    if(thirdTower.length!=0){
        delEvent(thirdTower[thirdTower.length - 1],"click", thirdTowerArrival);
    }

    round();
}

function addEvent(element, event, func) {
 
    if (element.addEventListener) { // Si notre élément possède la méthode addEventListener()
        element.addEventListener(event, func, true);
    } else { // Si notre élément ne possède pas la méthode addEventListener()
        element.attachEvent('on' + event, func);
    }
}
function delEvent(element, event, func) {
 
    if (element.removeEventListener) { // Si notre élément possède la méthode removeEventListener()
        element.removeEventListener(event, func, true);
    } else { // Si notre élément ne possède pas la méthode removeEventListener()
        element.detachEvent('on' + event, func);
    }
}

function mousePos( evt ){

    var Mouse_X = evt.pageX;
    var Mouse_Y = evt.pageY;
    transitorElt.style.bottom="calc(100% - "+(Mouse_Y-5)+"px)";
    transitorElt.style.left=""+(Mouse_X-16*parseInt(transitorElt.style.width)/2)+"px";
}