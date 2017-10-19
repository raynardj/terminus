
url_error_msg1="Staples Address Wrong"
$(document).ready(function(){
/*$(".auto_grab_showhide").hover(function(){
	$(this).css("color","#4682B4")
	$(this).css("background-color","#fff")
	$(this).css("border-color","#4682B4")
	$(this).css("font-weight","700")
})
$(".auto_grab_showhide").mouseleave(function(){
	$(this).css("color","#fff")
	$(this).css("background-color","#4682B4")
	$(this).css("border-color","#fff")
	$(this).css("font-weight","400")
})*/
$("input").focus(function(){
	var new_id=$(this).attr("id").replace("id","ex")
	if(new_id.indexOf("ex")!=-1)
	{
	$("#"+new_id).css("display","block");
	}
})
$("input").blur(function(){
	var new_id=$(this).attr("id").replace("id","ex")
	if(new_id.indexOf("ex")!=-1)
	{
	$("#"+new_id).css("display","none")
	}
})
$(".notice_slide_btn").hover(function(){
	$(this).css("opacity","1")
	$(".notice_slide_detail").css("display","block")
})
$(".notice_slide_btn").mouseleave(function(){
	$(this).css("opacity","0.5")
	$(".notice_slide_detail").css("display","none")
})
/*
$(".auto_grab_showhide").click(function(){
	if($(".grab_url_input").css("display")=="none")
	{
		$(".grab_url_input").show(300)
	}
	else
	{
		$(".grab_url_input").hide(300)
	}
})
*/
$(".try_grab").click(function(){
	var grab_url=$("#id_stburl").val()
	var proid=stb_url_valid(grab_url)
	ajax_from_url(grab_url,proid)
	})
})

function stb_url_valid(stburl)
// A function to extract product id from url
// Or return Error message
{
	var url_array=[]
	var url_array2=[]
	var url_array3=[]
	var rt=url_error_msg1
	url_array=stburl.split("staples.cn/product/")
	if(url_array[1])
		{
			url_array2=url_array[1].split("/")
			if(url_array2[0])
			{
				url_array3=url_array2[0].split("?")
				if(url_array3[0])
				{
					rt= url_array3[0]
				}
			}
		}
	return rt
}
function ajax_from_url(urlstb,pro_id)
{
	var rt
	if(pro_id==url_error_msg1)
	{}
	else
	{
		var inputdata={}
		inputdata.stburl=urlstb
		inputdata.pro_id=pro_id
		$("#aj_status").html("正在抓取,需要大约10秒...")
		$.ajax({
			url:'/ajaxofficeuse',
			data:inputdata,
			async:true,// So the ajax process does not stand in ways of other process
			method:'GET',
			success:function(data)
			{
				var rtjs=eval("("+data+")")
				$("#id_itemname").val(rtjs.itemname)
				$("#id_price").val(rtjs.price)
				$("#id_pro_id").val(rtjs.pro_id)
				$("#officeuse_pic").attr("src",rtjs.pic_src)
				$("#id_pic_src").val(rtjs.pic_src)
				$("#id_brandname").val(rtjs.brandname)
				$("#aj_status").html("抓取完毕")
			},//success function end,
			error:function()
			{
				$("#aj_status").html("未能从官网抓取 ,请检查官网链接,或手工填写下表:")
			}
		})//ajax end
	}//if else else end
}//func ajax_from_url end

