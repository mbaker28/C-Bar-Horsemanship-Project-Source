// This function is called after all HTML DOM elements have loaded:
$( document ).ready(function() {
    $("#section_reverse_never_ridden_seat").hide();
    $("#section_handpost_twopoint_circle").hide();
    $("#section_holds").hide();
    $("#section_shorten_lengthen_control_halt").hide();
    $("#section_stirrups_half_seat").hide();
    $("#section_post_proper").hide();
    $("#section_cavaletti_crossbar").hide();
    $("#section_overall_comments").hide();

    $("#section").change(function() {
        //alert("Section selection changed."); // DEBUGGING

        /*
            Show or hide the top category div tags if the right option is
            selected in the dropdown menu.
        */
        if ($("#section").val() == "section_basic_mount_aid") {
            //alert("Section selection is 'section_basic_mount_aid'."); // DEBUGGING
            $("#section_basic_mount_aid").show().siblings("div").hide();
            $("#section_basic_mount_aid").show().children().show();
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_reverse_never_ridden_seat") {
            //alert("Section selection is 'Reverse/Never-Ridden/Seat'."); // DEBUGGING
            $("#section_reverse_never_ridden_seat").show().siblings("div").hide();
            $("#section_reverse_never_ridden_seat").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_handpost_twopoint_circle") {
            //alert("Section selection is 'Hand-Post/Two-Point/Circle'."); // DEBUGGING
            $("#section_handpost_twopoint_circle").show().siblings("div").hide();
            $("#section_handpost_twopoint_circle").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_holds") {
            //alert("Section selection is 'Holds'."); // DEBUGGING
            $("#section_holds").show().siblings("div").hide();
            $("#section_holds").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_shorten_lengthen_control_halt") {
            //alert("Section selection is 'Shorten-Lengthen/Control/Halt'."); // DEBUGGING
            $("#section_shorten_lengthen_control_halt").show().siblings("div").hide();
            $("#section_shorten_lengthen_control_halt").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_stirrups_half_seat") {
            //alert("Section selection is 'Stirrups/Half-Seat'."); // DEBUGGING
            $("#section_stirrups_half_seat").show().siblings("div").hide();
            $("#section_stirrups_half_seat").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_post_proper") {
            //alert("Section selection is 'Post/Proper'."); // DEBUGGING
            $("#section_post_proper").show().siblings("div").hide();
            $("#section_post_proper").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_cavaletti_crossbar") {
            //alert("Section selection is 'Cavaletti/Crossbar'."); // DEBUGGING
            $("#section_cavaletti_crossbar").show().siblings("div").hide();
            $("#section_cavaletti_crossbar").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };
        if ($("#section").val() == "section_overall_comments") {
            //alert("Section selection is 'Overall Comments'."); // DEBUGGING
            $("#section_overall_comments").show().siblings("div").hide();
            $("#section_overall_comments").children().show(); // Show all the child elements
            $("#participant_info").show().children().show();
        };



    });
});
