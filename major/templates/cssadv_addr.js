//veriables
ter_server='http://{{host}}'
provinces={}
provinces["1"]="北京";provinces["2"]="甘肃";
provinces["3"]="河北";provinces["4"]="黑龙江";
provinces["5"]="吉林";provinces["6"]="辽宁";
provinces["7"]="内蒙古";provinces["8"]="山东";
provinces["9"]="山西";provinces["10"]="四川";
provinces["11"]="天津";provinces["12"]="新疆";
provinces["13"]="安徽";provinces["14"]="河南";
provinces["15"]="湖北";provinces["16"]="江苏";
provinces["17"]="陕西";provinces["18"]="上海";
provinces["19"]="浙江";provinces["20"]="福建";
provinces["21"]="广东";provinces["22"]="广西";
provinces["23"]="贵州";provinces["24"]="海南";
provinces["25"]="湖南";provinces["26"]="江西";
provinces["27"]="云南";provinces["28"]="重庆";
provinces["29"]="宁夏";provinces["30"]="青海";
provinces["31"]="西藏";
//build reversed object
provinces_r=reverse_object(provinces)

setTimeout(function(){
$(document).ready(function(){
	$(document).prepend(document.createElement("script").src="advcss_lib.js")
	console.log("AdvCSS address section:")
	load_css(ter_server+'/static/css/advcss_addr.css')
	var cp = document.createElement("div")
	cp.id="control"
  $(".header_txt").attr("id","advcss_platform")
  .html(cp)
  //load the address information again
  $.ajax({
      url:"/costCenter/addressInfo",
      method:"GET",
      data:{},
      async:false,
      success:function(data){
        $("#ajax_content").html(data);
        eid=disect_selection("escaladeId")
        prov_obj=disect_selection("provinceIdAdd")
        },
    })
  var adminsb=document.createElement("input")
  var sbtn=document.createElement("button")
  var jstb=document.createElement("table")
  jstb.id="jstb"
  adminsb.id="admin_search_bar"
  adminsb.type="text"
  sbtn.id="admin_search_btn"
  $(sbtn).html("search")
  $(cp).append(adminsb)
  .append(sbtn)
  .append(jstb)
  $("#admin_search_btn").click(function(){
    var admin=$("#admin_search_bar").val()
    var url=ter_server+'/cssadvjs?md=addr&admin='+admin;
    $.getJSON(url,function(json){
    load_users(json)
    })
  })
})
},1000)

//Functions:
function load_users(jsonreturn)
{
  var jsdata=jsonreturn.data
  console.log("The jsonp Data from Terminus II Server:")
  console.log(jsdata)
  $("#jstb").html("")
  for(var i=0;i<jsdata.length;i++)
  {
    $("#jstb").append(load_row(jsdata[i]))//see "load_row" function
  }
  if(jsdata.length >0 )
  {
  var pgbar=document.createElement("progress")
  var da_btn=document.createElement("button")//doall btn
  pgbar.id="users_progress_bar"
  pgbar.max=jsdata.length
  pgbar.value=0
  $(da_btn).html("Input All")
  $("#control").prepend(pgbar)
  $("#control").prepend(da_btn)
  $(da_btn).click({"bar":pgbar},function(e){
    $("#jstb").find("form").each(function(){
      var fmid=this.id
      var fmal=checkCargoAddress2(fmid)
      if(fmal.ct==0)
      {
        addCustInfos2(fmid);
      }
      else
      {
        $("#"+fmid).append("<div>"+fmal.errors+"</div>")
        $("#"+fmid+" input").css("background-color","red")
      }
      e.data.bar.value++
    })
  })
  }
}
function load_row(lineobj)
{
  /***
  Create form rows
  Digest lineobj, object containing a single entry info
  Spit out a html table row
  ***/
  var tr=document.createElement("tr")
  var td=document.createElement("td")
  var adfm=document.createElement("form")
  var ipt=[]
  adfm.id="addr_fm_"+lineobj.id
  adfm.action="/costCenter/addressInfo/add/"
  ipt[0]=document.createElement("select")
  ipt[1]=document.createElement("select")
  ipt[2]=document.createElement("select")
  ipt[3]=document.createElement("input")
  ipt[4]=document.createElement("input")
  ipt[5]=document.createElement("input")
  ipt[6]=document.createElement("input")
  ipt[0].name="escaladeId"
  ipt[1].name="provinceId"
  ipt[2].name="cityId"
  ipt[3].name="district"
  ipt[4].name="zip"
  ipt[5].name="cargoAddress"
  ipt[6].name="addCommonFlag"
  ipt[6].type="checkbox"
  ipt[6].value="1"
  ipt[0].className="escaladeId"
  ipt[1].className="provinceId"
  ipt[2].className="cityId"
  ipt[3].className="district"
  ipt[4].className="zip"
  ipt[5].className="cargoAddress"
  ipt[6].className="addCommonFlag"
  sub=document.createElement("button")
  sub.className="submit_line"
  //check10(ipt[6])
  //$(ipt[6]).click(function(){check10(ipt[6])})
  $(sub).html("Submit")
  $(sub).click({"formid":adfm.id},function(e){
    console.log(e.data.formid)
    addCustInfos2(e.data.formid);
  })
  var opt_e=[];var opt_p=[]
  for(var j=0;j<Object.keys(eid).length;j++)
  {
    opt_e[j]=document.createElement("option")
    $(opt_e[j]).attr("value",eid[Object.keys(eid)[j]])
      .html(Object.keys(eid)[j])
    if (Object.keys(eid)[j]==lineobj.clientname)
    {
      opt_e[j].selected="selected"
    }
    $(ipt[0]).append(opt_e[j])
  }
  for(var k=0;k<Object.keys(prov_obj).length;k++)
  {
    opt_p[k]=document.createElement("option")
    $(opt_p[k]).attr("value",prov_obj[Object.keys(prov_obj)[k]])
      .html(Object.keys(prov_obj)[k])
      if(Object.keys(prov_obj)[k]==lineobj.province)
      {
        opt_p[k].selected="selected"
        province_set_tocity(prov_obj[Object.keys(prov_obj)[k]],ipt[2],lineobj.city)// 3 parameters, 1st province code, second cityId select dom

      }
    $(ipt[1]).append(opt_p[k])
  }
  if(lineobj.area){ipt[3].value=lineobj.area;}
  if(lineobj.zip){ipt[4].value=lineobj.zip;}
  if(lineobj.address){ipt[5].value=lineobj.address;}
  if(lineobj.frequent){if(lineobj.frequent==1){ipt[6].checked="checked";}}
  //append to row:tr
  for(var i=0;i<ipt.length;i++)
  {
    $(adfm).append(ipt[i])
  }
  $(tr).html(td)
  $(td).html(adfm)
  $(td).append(sub)
  return tr
}
function read_line(formId)
{
	var dt=line_data(formId)
	console.log(dt)
}
function line_data(formId)
{
	//return the line data
	var fm=$("#"+formId)[0]
	var dt={};
	dt.escaladeId=$(fm).find("[name='escaladeId']")[0].value;
	dt.provinceId=$(fm).find("[name='provinceId']")[0].value;
	dt.cityId=$(fm).find("[name='cityId']")[0].value;
	dt.district=$(fm).find("[name='district']")[0].value;
	dt.zip=$.trim($(fm).find("[name='zip']")[0].value);
	dt.cargoAddress=$.trim($(fm).find("[name='cargoAddress']")[0].value);
	return dt	
}
function alertinfo(formId)
{
  // An object class
  // to handle alert action
  this.msg=document.createElement("div")
  this.ct=0
  this.formId=formId
  this.errors=""
  $(this.msg).html("发现以下问题")
  this.ac=function(inputName,newEntry){
    this.ct++
    var ne=document.createElement("div")
    $(ne).append(newEntry)
    ne.className="alert_line"
    $("#"+this.formId+" [name='"+inputName+"']").css("background-color","#FFDAB9")
    .css("box-shadow","0px 0px 5px #CD5C5C inset")
    $(this.msg).append(ne)
    console.log(inputName+" checked: Error")
    var uid=this.formId.split("_")[2]
    this.errors=this.errors+"<br>"+newEntry
    var url=ter_server+'/cssadvjs?md=errormsg&uid='+uid+'&errormsg='+newEntry;
    $.getJSON(url,function(json){
    })
  }
  this.lay=function(parent_Obj_id){
    //Print out the alert info
    if (this.ct>0)//Has alert
    {
      // Print out the accumulated alert info
      $("#"+parent_Obj_id).html(this.msg)
      var c_err=[]
      $(".alert_line").each(function(){
        c_err.push($(this).text());
      })
      $("#"+parent_Obj_id).data("c_err",c_err)
    }
    else//Check passed
    {
      $("#"+parent_Obj_id).html("<div class='gw'>All Checked</div>")
      //$(".replicate_input").attr("disabled","disabled")
    }
  }
}
function checkCargoAddress2(formId){
	//check the line data
	// return the alert info object
		    var dt=line_data(formId)
        var provinceIdAdd = dt.provinceId;
        var cityIdAdd = dt.cityId;
        var districtAdd = dt.district;
        var zipAdd = dt.zip;
        var cargoAddressAdd = dt.cargoAddress;
        var al=new alertinfo(formId)
        if($.trim(provinceIdAdd)=="" || $.trim(provinceIdAdd)=="0")
        	{al.ac("provinceId","请选择省份");}
        if($.trim(cityIdAdd)=="" || $.trim(cityIdAdd)=="0")
        	{al.ac("cityId","请选择城市");}
        if(zipAdd==''||zipAdd=='邮编')
        	{al.ac("zip",'请输入邮编');}
        if(zipAdd.length<6)
        	{al.ac("zip",'输入邮编长度不够');}
        if(isNaN(zipAdd)||zipAdd.indexOf('.')>=0||zipAdd.indexOf('-')>=0)
        	{al.ac("zip",'输入邮编格式不正确');}
        if(cargoAddressAdd.length<1 || cargoAddressAdd=='详细地址')
        	{al.ac("cargoAddress","请输入详细地址");}
        if(cargoAddressAdd.length>50)
        	{al.ac("cargoAddress","详细地址输入字数不能超过50");}
        if(dt.escaladeId=="")
        	{al.ac("escaladeId",'请选择结算单位');}
        return al;
    }
function province_set(p_select)
{
 var province=p_select.value;
 var c_select=$(p_select).next("select [name='cityId']")[0]; 
 $(c_select).load("/getCityByPid?parentId="+prov_obj[province]); 
}
function province_set_tocity(pro_value,c_select,c_text)
{
  //console.log("/getCityByPid?parentId="+String(pro_value))
  var dt={}
  dt.c_text=c_text
  $(c_select).load("/getCityByPid?parentId="+String(pro_value),dt,function(){
    var ops=c_select.options
    for(var i=0;i<ops.length;i++)
    {
      if($(ops[i]).text()==dt.c_text)
      {
        ops[i].selected="selected"
      }
    }
    });

}
function addCustInfos2(formId){
        var addFormData = $('#'+formId).serialize();
        var doAction = $('#'+formId).attr('action');
        midglo=formId.split("_")[2]
        // $.post(doAction+"",addFormData,function(data){
        //     if(data=="1"){
        //         console.log("submited")
        //         var url=ter_server+'/cssadvjs?md=fbdone&uid='+midglo;
        //         $.getJSON(url,function(json){})
        //         //doSearch();
        //         // $('#provinceIdAdd').val('');
        //         // $('#cityIdAdd').val('');
        //         // $('#districtAdd').val('区域');
        //         // $('#zipAdd').val('邮编');
        //         // $('#cargoAddressAdd').val('详细地址');
        //     }
        //     else{
        //         console.log("submit_error")
        //         console.log(data);
        //            var url=ter_server+'/cssadvjs?md=errormsg&uid='+midglo+'&errormsg='+data;
        //           $.getJSON(url,function(json){
        //           })              
        //     }
        // });

        $.ajax({
          url:doAction+"",
          data:addFormData,
          method:"POST",
          async:false,
          success:function(data){
            if(data=="1"){
                console.log("submited")
                var url=ter_server+'/cssadvjs?md=fbdone&uid='+midglo;
                $.getJSON(url,function(json){})
                //doSearch();
                // $('#provinceIdAdd').val('');
                // $('#cityIdAdd').val('');
                // $('#districtAdd').val('区域');
                // $('#zipAdd').val('邮编');
                // $('#cargoAddressAdd').val('详细地址');
            }
            else{
                console.log("submit_error")
                console.log(data);
                   var url=ter_server+'/cssadvjs?md=errormsg&uid='+midglo+'&errormsg='+data;
                  $.getJSON(url,function(json){
                  })
              $("#addr_fm_"+midglo).append("<div>"+data+"</div>")              
              $("#addr_fm_"+midglo).css("background-color","red")              
            }
        },
      });
    }

function readcity(provinceId)
{
	var ajdt={}
	ajdt.parentId=provinceId
	$.ajax({
		url:"/getCityByPid",
		data:ajdt,
		async:false,
		method:"GET",
		success:function(){
			console.log()
		}
	})
}

function load_css(css_url)
{
  //variable DOM Style to print css 
  //Make sure there is a <head> tag
  var dcss=document.createElement("style")
  $(dcss).attr("type","text/css")
  $(dcss).html("@import url('"+css_url+"')")
  $("head").append(dcss)
  console.log("CSS deployed:["+css_url+"]")
}
function disect_selection(selectionId)
{
	//selection id like:searchEscaladeId
  //compact in to object like {"text":"value"}
	var oplist={}
	var i=0
	$("#"+selectionId).find("option").each(function(){
		oplist[$(this).text()]=$(this).val();
		i++
	})
	//console.log(oplist)
	return oplist
}

function reverse_object(obja)
{
	// reverse {a:b} to {b:a}
	var objb={}
	var kys=Object.keys(obja)
	for(var i=0;i<kys.length;i++)
	{
		objb[obja[kys[i]]]=kys[i]
	}
	return objb
}


// function doSearch(){
// 	// for reference
//         var url="/costCenter/addressInfo";
//         var searchEscaladeId = $.trim($("#searchEscaladeId").val());
//         var provinceId = $("#provinceId").val();
//         var cityId = $("#cityId").val();
//         var cargoAddressStr = $.trim($("#cargoAddressStr").val());
//         var data =  {"flag":1,"provinceId":provinceId,"cityId":cityId,"cargoAddress":cargoAddressStr,"escaladeId":searchEscaladeId};


//         $.ajax({
//             url : url,
//             data: data,
//             type : "POST",
//             cache: false,
//             dataType : "html",
//             async:false,
//             success : function (data){
//                 if(null!=data){
//                     $("#searchResult").html(data);
//                 }
//             }
//         });
//     }