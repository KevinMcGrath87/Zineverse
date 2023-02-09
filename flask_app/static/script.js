function size_up(element){
    element.height = "500px";
}
function size_down(element){
    element.style.height = toString(element.style.height /2)+"px";
    console.log(element.style.height)
}
