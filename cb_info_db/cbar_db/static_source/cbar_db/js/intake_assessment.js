// This function is called after all HTML DOM elements have loaded:
$( document ).ready(function() {
    $("#premounted").hide();

    $("#section").change(function() {
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
        if ($("#section").val() == "premounted_behavior") {
            // alert("Section selection is 'premounted_ambulatory'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#behavior").show().siblings("div").hide();
        };
        if ($("#section").val() == "communication_verbal") {
            // alert("Section selection is 'premounted_ambulatory'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#communication_verbal").show().siblings("div").hide();
        };
        if ($("#section").val() == "communication_visual") {
            // alert("Section selection is 'premounted_ambulatory'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#communication_visual").show().siblings("div").hide();
        };
        if ($("#section").val() == "communication_hearing") {
            // alert("Section selection is 'premounted_ambulatory'."); // DEBUGGING
            $("#premounted").show().siblings("div").hide();
            $("#communication_hearing").show().siblings("div").hide();
        };
    });
});
