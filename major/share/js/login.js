// JavaScript Document
// js file at the end of login/register/reset page
$(document).ready(function() {
	// Hover on button
    $("#subm_btn,.link_div").hover(function(){
		$(this).css("box-shadow","0px 0px 5px hsla(180,50%,1%,0.7) inset")
		$(this).css("border-color","hsla(180,50%,99%,0.3)")
		})
    // Mouse leave button
	$("#subm_btn,.link_div").mouseleave(function(){
		$(this).css("box-shadow","0px 0px 0px 0px hsla(180,50%,1%,0.7) inset")
		$(this).css("border-color","hsla(180,50%,99%,0)")
		})
    // Shrink and fade effect of background picture
    $("input").click(function(){
        $(".bg_pic_img").animate({width:"110%",top:"-30px",left:"-70px",opacity:"0.5"},300)
    })
});