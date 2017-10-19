$(document).ready(function(){
	var pro_id=$("#id_pro_id").val()
	var stburl="www.staples.cn/product/"+pro_id
	$("#id_stburl").val(stburl)
	$(".try_grab").click()
})