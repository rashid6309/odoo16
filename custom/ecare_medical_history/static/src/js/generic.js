
/* This function will navigate to provided element id */
function scrollToElement(element_id){
    /*
        element_id: unique id(str) of the element
    */
    setTimeout(function() {
        var innerDiv = document.getElementById(element_id);
        if (innerDiv) {
            var repeatConsultationElement = document.getElementById('repeat_consultation_working_state');
            if(!repeatConsultationElement)
            {
                innerDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    }, 600);

}

function toggle_element_icon_class(element, icon_first, icon_second){
    $(element).find('i').toggleClass(icon_first).toggleClass(icon_second);
}

//This is generic function which is taking element ID as parameter and showing the complete div
//which is intitially collapsed to show state

function showRepeatConsultationSection(element_id) {
    var targetDiv = document.getElementById(element_id);
    targetDiv.classList.add("show");
    return false;
}