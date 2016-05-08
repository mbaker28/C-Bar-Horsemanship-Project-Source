// This function is called after all HTML DOM elements have loaded:
$( document ).ready(function() {
    $("#premounted").hide();
    $("#sidewalkers_required").hide();

    $("#section").change(function() {
        // alert("Section selection changed."); // DEBUGGING

        /*
            Show or hide the top category div tags if the right option is
            selected in the dropdown menu.
        */
        if ($("#section").val() == "general_information") {
            // alert("Section selection is 'general_information'."); // DEBUGGING
            $("#general_information").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted") {
            // alert("Section selection is 'premounted'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#premounted").children().show(); // Show all the child elements
        };
        if ($("#section").val() == "sidewalkers_required") {
            // alert("Section selection is 'sidewalkers_required'."); // DEBUGGING
            $("#sidewalkers_required").show().siblings("div").hide();
        };

        /*
            Show or hide the second-to-top category div tags if the right option
            is selected in the dropdown menu.
        */
        if ($("#section").val() == "premounted_posture") {
            // alert("Section selection is 'premounted_posture'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#posture").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted_ambulatory") {
            // alert("Section selection is 'premounted_ambulatory'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#ambulatory").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted_gait") {
            // alert("Section selection is 'premounted_gait'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#gait").show().siblings("div").hide();
        };
    });
});
