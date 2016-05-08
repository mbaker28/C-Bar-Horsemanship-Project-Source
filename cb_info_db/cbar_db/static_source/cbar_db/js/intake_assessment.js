// This function is called after all HTML DOM elements have loaded:
$( document ).ready(function() {
    $("#premounted").hide();

    $("#section").change(function() {
        /*
            Show or hide the top category div tags if the right option is
            selected in the dropdown menu.
        */
        if ($("#section").val() == "general_information") {
            $("#general_information").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted") {
            $("#premounted").show().siblings("div").hide();
            $("#premounted").children().show(); // Show all the child elements
        };

        /*
            Show or hide the second-to-top category div tags if the right option
            is selected in the dropdown menu.
        */
        if ($("#section").val() == "premounted_posture") {
            $("#premounted").show().siblings("div").hide();
            $("#posture").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted_ambulatory") {
            $("#premounted").show().siblings("div").hide();
            $("#ambulatory").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted_behavior") {
            $("#premounted").show().siblings("div").hide();
            $("#behavior").show().siblings("div").hide();
        };
        if ($("#section").val() == "communication_verbal") {
            $("#premounted").show().siblings("div").hide();
            $("#communication_verbal").show().siblings("div").hide();
        };
        if ($("#section").val() == "communication_visual") {
            $("#premounted").show().siblings("div").hide();
            $("#communication_visual").show().siblings("div").hide();
        };
        if ($("#section").val() == "communication_hearing") {
            $("#premounted").show().siblings("div").hide();
            $("#communication_hearing").show().siblings("div").hide();
        };
        if ($("#section").val() == "tactile") {
            $("#premounted").show().siblings("div").hide();
            $("#tactile").show().siblings("div").hide();
        };
        if ($("#section").val() == "motor_skills") {
            $("#premounted").show().siblings("div").hide();
            $("#motor_skills").show().siblings("div").hide();
        };
    });
});
