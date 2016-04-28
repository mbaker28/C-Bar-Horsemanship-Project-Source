// This function is called after all HTML DOM elements have loaded:
$( document ).ready(function() {
    $("#premounted").hide();
    $("#sidewalkers_required").hide();

    $("#section").change(function() {
        alert("Section selection changed.");

        if ($("#section").val() == "general_information") {
            alert("Section selection is 'general_information'.");
            $("#general_information").show().siblings("div").hide();
        };
        if ($("#section").val() == "premounted") {
            alert("Section selection is 'premounted'.");
            $("#premounted").show().siblings("div").hide();
        };
        if ($("#section").val() == "sidewalkers_required") {
            alert("Section selection is 'sidewalkers_required'.");
            $("#sidewalkers_required").show().siblings("div").hide();
        };
    });
});
