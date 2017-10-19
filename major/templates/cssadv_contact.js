// JavaScript Document

ter_server='http://{{host}}'
setTimeout(function(){
$(document).ready(function(){
var btnbar=document.createElement("div")
btnbar.className="topcontrolbar"
/*$(btnbar).css("position","fixed")*/

$(btnbar).css("background-color","#EEE")
$(btnbar).css("padding","10px")
$(btnbar).css("box-shadow","0px 0px 5px #aaa")
$(btnbar).css("height","200px")
$(btnbar).css("width","100%")
$(".header_txt").html(btnbar)
$(".header_txt").css("height","200px")

// put on the buttons
var btnctt="<input type='text' id='client_input_jsonp' style='width:150px;margin:5px;padding:2px;border:1px solid #fff;'/>"
btnctt=btnctt+"<button onclick='get_contact_data()'>Start</button>"
btnctt=btnctt+"<div id='contact_json_penal' style='height:150px;overflow:auto'></div>"
$(btnbar).append(btnctt)


//checkReceiverInfo2()
//expand_root()
//setTimeout(function(){analyze_treeDemo()},1000)
})
},2000)

function logTest() {
    console.log("Being called from " + arguments.callee.caller.toString());
}
function read_cookie()
// Return the cookie info on console
{

	console.log(document.cookie)
}
function get_contact_data()
{
	var dt={}
	dt.uid=$("#client_input_jsonp").val()
	dt.md='contact'
	var url=ter_server+'/cssadvjs?md=contact&uid='+dt.uid;
	$.getJSON(url,function(json){
		load_contact(json)
		})
}
function load_contact(json)
{
	var data=json.data
	var dttable=document.createElement("div")
	var tbs=[]
	var rows=[]
	var tds=[]
	var ipts=[]
	var forms=[]
	var firsttr=document.createElement("tr")
	var firsttd=document.createElement("td")
	$(firsttd).attr("colspan",3)
	var runallbtn=document.createElement("button")
	var breakrunbtn=document.createElement("button")
	var ct_mark=document.createElement("span")
	ct_mark.id="contact_mark"
	$(firsttd).append(ct_mark)
	$(runallbtn).click(function(){receiver_line_addall()})
	$(runallbtn).html("上传所有")
	$(breakrunbtn).click(function(){break_addall()})
	$(breakrunbtn).html("中止上传")
	$(firsttr).append(firsttd)
	$(firsttd).append(runallbtn)
	//$(firsttd).append(breakrunbtn)
	$(dttable).append(firsttr)
	for(var i=0;i<json.data.length;i++)
	{
		rows[i]=document.createElement("tr")
		tds[i]=[]
		ipts[i]=[]
		tbs[i]=document.createElement("table")
		rows[i].id=json.data[i]._id
		forms[i]=document.createElement("form")
		forms[i].id="addForm_"+rows[i].id;
		forms[i].action="/costCenter/receiverInfo/add/";
		$(forms[i]).attr("onsubmit","return false;");
		rows[i].className="contact_json_row"
		// Name
		tds[i]["name"]=document.createElement("td")
		tds[i]["name"].className="xb2_name"
		ipts[i]["name"]=document.createElement("input")
		ipts[i]["name"].type="text"
		ipts[i]["name"].name="receiverName"
		ipts[i]["name"].className="xb2_ipt_name"
		$(ipts[i]["name"]).css("width","100px")
		$(tds[i]["name"]).html(ipts[i]["name"])
		if(json.data[i].name){$(ipts[i]["name"]).val(json.data[i].name);}
		// Phone
		tds[i]["phone"]=document.createElement("td")
		tds[i]["phone"].className="xb2_phone"
		ipts[i]["phone"]=document.createElement("input")
		ipts[i]["phone"].type="text"
		ipts[i]["phone"].name="receiverPhone"
		ipts[i]["phone"].className="xb2_ipt_phone"
		$(ipts[i]["phone"]).css("width","110px")
		$(tds[i]["phone"]).html(ipts[i]["phone"])
		if(json.data[i].phone){$(ipts[i]["phone"]).val(json.data[i].phone);}
		// cellphone
		tds[i]["cellphone"]=document.createElement("td")
		tds[i]["cellphone"].className="xb2_cellphone"
		ipts[i]["cellphone"]=document.createElement("input")
		ipts[i]["cellphone"].type="text"
		ipts[i]["cellphone"].name="receiverCellphone"
		ipts[i]["cellphone"].className="xb2_ipt_cellphone"
		$(ipts[i]["cellphone"]).css("width","110px")
		$(tds[i]["cellphone"]).html(ipts[i]["cellphone"])
		if(json.data[i].cellphone){$(ipts[i]["cellphone"]).val(json.data[i].cellphone);}
		// fax
		tds[i]["fax"]=document.createElement("td")
		tds[i]["fax"].className="xb2_fax"
		ipts[i]["fax"]=document.createElement("input")
		ipts[i]["fax"].type="text"
		ipts[i]["fax"].name="fax"
		ipts[i]["fax"].className="xb2_ipt_fax"
		$(ipts[i]["fax"]).css("width","100px")
		$(tds[i]["fax"]).html(ipts[i]["fax"])
		if(json.data[i].fax){$(ipts[i]["fax"]).val(json.data[i].fax);}
		// email
		tds[i]["email"]=document.createElement("td")
		tds[i]["email"].className="xb2_email"
		ipts[i]["email"]=document.createElement("input")
		ipts[i]["email"].type="text"
		ipts[i]["email"].name="emailAddr"
		ipts[i]["email"].className="xb2_ipt_email"
		$(ipts[i]["email"]).css("width","100px")
		$(tds[i]["email"]).html(ipts[i]["email"])
		if(json.data[i].email){$(ipts[i]["email"]).val(json.data[i].email);}
		// button
		tds[i]["btn"]=document.createElement("button")
		$(tds[i]["btn"]).text("Fill")
		$(tds[i]["btn"]).data("id",json.data[i]._id)
		$(tds[i]["btn"]).click(function(){fill_in_contact($(this).data("id"))})
		// Create Remove Button
		tds[i]["rmbtn"]=document.createElement("button")
		$(tds[i]["rmbtn"]).text("去除")
		$(tds[i]["rmbtn"]).data("id",json.data[i]._id)
		$(tds[i]["rmbtn"]).click(function(){receiver_line_detask($(this).data("id"))})		
		tds[i]["btntd"]=document.createElement("td")
		tds[i]["btntd"].append(tds[i]["btn"])
		tds[i]["btntd"].append(tds[i]["rmbtn"])
		tds[i]["btntd"].className="xb2_btn"
		tds[i]["react"]=document.createElement("td")
		tds[i]["react"].className="xb2_react"
		$(tds[i]["react"]).data("status","0")
		$(tds[i]["react"]).text("Waiting")

		//combine
		$(rows[i]).append(tds[i]["name"])
		$(rows[i]).append(tds[i]["phone"])
		$(rows[i]).append(tds[i]["cellphone"])
		$(rows[i]).append(tds[i]["fax"])
		$(rows[i]).append(tds[i]["email"])
		$(rows[i]).append(tds[i]["btntd"])
		$(rows[i]).append(tds[i]["react"])
		$(tbs[i]).append(rows[i])
		$(forms[i]).append(tbs[i])
		$(dttable).append(forms[i])
	}
	$("#contact_json_penal").html(dttable)
}
function fill_in_contact_first()
{
	if ($("#contact_json_penal").find(".contact_json_row"))
	{
	var uid=$("#contact_json_penal").find(".contact_json_row").first().attr("id")
	console.log("prepare:"+uid)
	fill_in_contact(uid)
	}
	else
	{
		break_addall()
	}
}
function fill_in_contact(userid)
{
	//Show running
	$("#"+userid).find(".react").html("正在运行")
	// var name=$("#"+userid).find(".xb2_name").text()
	// var phone=$("#"+userid).find(".xb2_phone").text()
	// var cellphone=$("#"+userid).find(".xb2_cellphone").text()
	// var fax=$("#"+userid).find(".xb2_fax").text()
	// var email=$("#"+userid).find(".xb2_email").text()
	// $("#receiverNameAdd").attr("value",name)
	// $("#receiverPhoneAdd").attr("value",phone)
	// $("#receiverCellphoneAdd").attr("value",cellphone)
	// $("#faxAdd").attr("value",fax)
	// $("#emailAddrAdd").attr("value",email)
	//Check data
	if(checkReceiverInfo2(userid)==true)
	{
	//run the add function
	addCustInfos2(userid)
	}
	else
	{
		break_addall()
	}
}
function analyze_treeDemo()
{
 treelinks=[]
 var spans=$("#treeDemo").find("span")
 console.log(spans.length+" spans found in total")
 for(var i=0;i<spans.length;i++)
 {
 	treelinks[i]=[]
 	treelinks[i]["txt"]=$(spans[i]).text()
 	treelinks[i]["aid"]=$(spans[i]).parent("a").attr("id")
 	treelinks[i]["exp"]=treelinks[i]["aid"].replace("_a","_switch") 	
 	console.log(treelinks[i]["txt"]+"|"+treelinks[i]["aid"]+"|"+treelinks[i]["exp"])
 }
}
function click_cost_center(cost_center_name)
{
 	for(var i=0;i<treelinks.length;i++)
 	{
 		if(treelinks[i]["txt"]==cost_center_name)
 		{
 			$("#"+treelinks[i]["aid"]).click()
 		}
 	}
}
function expand_cost_center(cost_center_name)
{
	for(var i=0;i<treelinks.length;i++)
 	{
 		if(treelinks[i]["txt"]==cost_center_name)
 		{
 			$("#"+treelinks[i]["exp"]).click()
 			analyze_treeDemo()
 		}
 	}
}
function addCustInfos2(uid){
	/* 
	Enter one line of information, altered form the original JS function: addCustInfos()
	Argument is the user id(mgid)
	*/
		var addFormData = $('#addForm_'+uid).serialize();
		var doAction = $('#addForm_'+uid).attr('action');
		$.post(doAction+"4",addFormData,function(data){
			if(data=="1"){// if the upload is successful
				$.getJSON(ter_server+"/cssadvjs?md=fbdone&uid="+uid,function(json){
					console.log(json.fb);			
				})
				$("#"+uid).attr("class","contact_json_row_done")
				$("#"+uid).find(".xb2_react").html("完成")
				$("#"+uid).find(".xb2_btn").html("-")
				// Disable the input boxes
				$("#"+uid).find("input").each(function(){$(this).attr("disabled","true")})
				ajaxPage('/costCenter/receiverInfo');
				return true
    		}
    		else{
    			// If error occured in the JS process
    			break_addall();
    			console.log(data);
    			alert(data);
    		}
    	});
	}

function receiver_line_addall()
{
	interval_contact=window.setInterval("fill_in_contact_first()",600)
}

function break_addall()
{
	window.clearInterval(interval_contact)
}
function receiver_line_detask(uid)
{
	// Remove 1 entry from the server by uid
	$.getJSON(ter_server+"/cssadvjs?md=fbremove&uid="+uid,function(json){
				console.log(json.fb);$("#"+uid).find(".xb2_name").html("")
				$("#"+uid).remove();
				})	
}
function checkReceiverInfo2(uid){
	console.log("checking:"+uid)
	$.ajaxSetup({async:false});
		var receiverNameAdd = $('#addForm_'+uid).find(".xb2_ipt_name");
		console.log($(receiverNameAdd).val())
		var receiverPhoneAdd = $('#addForm_'+uid).find(".xb2_ipt_phone");
		console.log($(receiverPhoneAdd).val())
		var receiverCellphoneAdd = $('#addForm_'+uid).find(".xb2_ipt_cellphone");	
		console.log($(receiverCellphoneAdd).val())
		if($.trim($(receiverNameAdd).val())==""){
			break_addall()
			alert('请输入姓名!');
			return false;
		}
		if($.trim($(receiverPhoneAdd).val())=="" && $.trim($(receiverCellphoneAdd).val())==""){
			break_addall()
			alert('请输入电话或手机号!');
			return false;
		}
		return true;
	}
function expand_root()
{
	console.log("click expand root")
	$("#treeDemo_1_switch").click()
}
function chooseApprover(id){
if(id!='undefined'&&id!=null){
		var url='/costCenter/approverTree/'+id;
	}else{
		var url='/costCenter/approverTreeByInsert'
	}
	loadChooseApproverTree(url);
/*	if(zNodesApproverDialog==null){
		//alert("zNodesApproverDialog==null");
		loadChooseApproverTree(url);
	}else{
		//alert("zNodesApproverDialog!=null");
		//alert($("#treeApproverDialog").html());
		//$.fn.zTree.init($('#treeApproverDialog'), settingDialog, zNodesApproverDialog);
		//var zTreeApproverDialog = $.fn.zTree.getZTreeObj("treeApproverDialog");
		//zTreeApproverDialog.expandAll(true);//完全展开
		 openDialog('#select-approverBox', '选 择 审批人', 400, 500);
	}*/
}
function loadChooseApproverTree(url){
	var request = $.ajax({
		url : url,
		beforeSend : null,
		type : "POST",
		cache: false,
		dataType : "json"
	});
	var treeApproverDialog = $("#treeApproverDialog");
	if($.trim(treeApproverDialog.html())==""){
		
		request.done(function(data) {
			if (data.result == "200") {
				treeApproverDialog.html("");
				zNodesApproverDialog=data.resultMap.tree;
				$.fn.zTree.init(treeApproverDialog, settingDialog, zNodesApproverDialog);
				var zTreeApproverDialog = $.fn.zTree.getZTreeObj("treeApproverDialog");
				zTreeApproverDialog.expandAll(true);//完全展开
				openDialog('#select-approverBox', '选 择 审批人', 550, 500);
				
			}else{
				//alert("Request failed: " + textStatus);
			}
		});
		
		request.fail(function(jqXHR, textStatus) {
			//alert("Request failed: " + textStatus);
			location.reload();
		});
	}else{
		openDialog('#select-approverBox', '选 择 审批人', 550, 500);
	}
}

function updateOrSaveCost(url) {
	commonAlert($("form[name='cost_center_form']").text())
	var inputs = $("form[name='cost_center_form']").find(":input");
	var flag=0;
	
	var radioChecked = $("#approve_radios").find(":input:checked");
	
	var approveAmt = $.trim($('#approveAmt').val());
	
	var msg="请填写完整信息";
	var count = 0;
	
	var ccName = $.trim($('#ccName').val());
	if(ccName==""){
		commonAlert('请输入成本中心名称!');
		return false;
	}
	if(ccName.length>20){
		commonAlert('成本中心名称长度不能超过20个字!');
		return false;
	}
	if($.trim(radioChecked.val())==""){
		commonAlert("请选择‘是否要审批!");
		return false;
	}
	
	if($.trim(radioChecked.val())=="0" || $.trim(radioChecked.val())=="2"){
		if($.trim($('#selectContent').val())==""){
			commonAlert("请选择审批人!");
			return false;
		}
		if(approveAmt!="" && (isNaN(approveAmt) || approveAmt<0)){
			commonAlert("请输入正确的审批金额!");
			return false;
		}

		if(approveAmt.indexOf('.')>=0){
			commonAlert("审批金额必须为整数!");
			return false;
		}
		
		if($.trim($('#approveAmt').val())==""){
			commonAlert("请输入审批金额!");
			return false;
		}
	}
	
	if(flag==0){
		if(checkApproveAmt()){
			var goal_options = {
					target : null,
					beforeSubmit : null,
					success : function(data) {
						if(data.result == "500"){
							commonAlert("成本中心名称已经存在");
						}else{
//							reFlahTree(data);
							if (data.result == "updateOk") {
								commonAlert("修改成功!新提交信息将在后台审核之后才能生效.");
							}else if(data.result == "insertOk"){
								commonAlert("新增成功!新提交信息将在后台审核之后才能生效.");
								ajaxPage('/costCenter/costCenterEdit/'+data.resultMap.costId,null,null,'costRightInfo');
								var before_fn= function (){
									update_cost_user_class('cost');
								} ;
							}
							//doFormSubmit("search_all", "/costCenter/costCenterList", null, "costRightInfo", null, null);
						}
					},
					type : "post"
			};
			
			goal_options.url = url;
			$("form[name='cost_center_form']").ajaxSubmit(goal_options);
		}
	}
}
