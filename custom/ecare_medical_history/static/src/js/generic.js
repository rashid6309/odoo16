
/* This function will navigate to provided element id */
function scrollToElement(element_id){
    /*
        element_id: unique id(str) of the element
    */
    setTimeout(function() {
        var innerDiv = document.getElementById(element_id);
        if (innerDiv) {
            innerDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 1000);

}

function showRepeatConsultationSection() {
    var targetDiv = document.getElementById("repeat_consultation_section");
    targetDiv.classList.add("show");
    return false;
}
