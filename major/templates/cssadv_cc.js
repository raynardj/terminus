// Created by Cool CTO --JS Engineer Jamie J
// JavaScript Document 
/*
Advantage CSS data auto-filling
[Cost Center Page]
1143*/

console.log('===JS file [advcss_cc.js] loaded===');
ter_server='http://{{host}}'

user_jsp_dt={}
up_dict={}
/*User Property Dictionary*/
up_dict["绑定成本中心"]="costArrayStr";
up_dict["登录名"]="userSysName";
up_dict["密码"]="password";
up_dict["确认密码"]="confirm_password";
up_dict["姓名"]="userRealName";
up_dict["性别"]="sex";
up_dict["联系电话1"]="dftPhone1";
up_dict["分机1"]="dftPhone1Ext";
up_dict["联系电话2"]="dftPhone2";
up_dict["分机2"]="dftPhone2Ext";
up_dict["传真"]="faxNbr";
up_dict["分机3"]="faxNbrExt";
up_dict["手机"]="cellPhoneNbr";
up_dict["Email"]="userEmail";
up_dict["办公耗材"]="userProdAccessList[0].status";
up_dict["电脑及配件"]="userProdAccessList[1].status";
up_dict["通讯设备/手机"]="userProdAccessList[2].status";
up_dict["通讯设备"]="userProdAccessList[2].status";
up_dict["食品饮料"]="userProdAccessList[3].status";
up_dict["劳防用品"]="userProdAccessList[4].status";
up_dict["卡券及商务礼品"]="userProdAccessList[5].status";
up_dict["办公用纸"]="userProdAccessList[6].status";
up_dict["办公文具"]="userProdAccessList[7].status";
up_dict["办公设备"]="userProdAccessList[8].status";
up_dict["数码设备"]="userProdAccessList[9].status";
up_dict["办公家电"]="userProdAccessList[10].status";
up_dict["生活用品"]="userProdAccessList[11].status";
up_dict["办公家具"]="userProdAccessList[12].status";
up_dict["审批方式"]="isNeetApprove";
up_dict["审批人"]="approveArrayStr";
up_dict["审批金额"]="approveAmt";
up_dict["单笔订单采购限额"]="oneorderLmtAmt";
up_dict["财政年起始月份"]="startMonth";
up_dict["月采购限额有无"]="monthlimit";
up_dict["月采购限额"]="monthlyLmtAmt";
up_dict["月采购余额跨月累计"]="isCumulateMonthLmt";
up_dict["季度采购额度"]="quarterLimitFlag";
up_dict["Q1"]="quarterQ1Amt"; up_dict["Q2"]="quarterQ2Amt";
up_dict["Q3"]="quarterQ3Amt"; up_dict["Q4"]="quarterQ4Amt";
up_dict["季采购余额跨月累计"]="quarterAccumulativeFlag";
up_dict["年采购限额有无"]="yearlimit";
up_dict["年采购限额"]="yearlyLmtAmt";
up_dict["查看报表"]="isAcsRpt";
up_dict["显示热销商品"]="isDispRecomprod";
up_dict["显示广告banner"]="isDispSalePrmt";
up_dict["成本中心名称"]="ccName";
up_dict["描述"]="description";
up_dict["上级成本中心"]="highlvCcId";
up_dict["是否需要审批"]="isNeetApprove";
console.log("===User property dict loaded===")
//v_dict for function translate_user_jp
c_dict={}
c_dict["审批人"]="approveArrayStr"
c_dict["成本中心名称"]="ccName"
c_dict["描述"]="description"
c_dict["上级成本中心"]="highlvCcId"
c_dict["审批金额"]="approveAmt"
c_dict["是否需要审批"]="isNeetApprove"
console.log("===Cost Center property dict loaded===")
v_dict_cate={}
v_dict_cate["kw"]=[
    "userProdAccessList[0].status",
    "userProdAccessList[1].status","userProdAccessList[2].status",
    "userProdAccessList[3].status","userProdAccessList[4].status",
    "userProdAccessList[5].status","userProdAccessList[6].status",
    "userProdAccessList[7].status","userProdAccessList[8].status",
    "userProdAccessList[9].status","userProdAccessList[10].status",
    "userProdAccessList[11].status","userProdAccessList[12].status"]
v_dict_cate["所有"]=2
v_dict_cate["协议"]=0
v_dict_cate["不可见"]=1
console.log("===Value Translation Dictionary [Category] Loaded===")

v_dict_approve={}
v_dict_approve['kw']=['isNeetApprove']
v_dict_approve["按成本中心审批"]=0
v_dict_approve["按用户审批"]=2
v_dict_approve["不审批"]=1
console.log("===Value Translation Dictionary [Approve] Loaded===")

v_dict_hasnot={}
v_dict_hasnot['kw']=[
    "monthlimit",
    "quarterLimitFlag"
]
v_dict_hasnot["有"]=0
v_dict_hasnot["无"]=1
console.log("===Value Translation Dictionary [Has/Not] Loaded===")

v_dict_yesno={}
v_dict_yesno["kw"]=[
"isCumulateMonthLmt","quarterAccumulativeFlag",
"isAcsRpt","isDispRecomprod","isDispSalePrmt"
]
v_dict_yesno["是"]=0
v_dict_yesno["否"]=1
console.log("===Value Translation Dictionary [Yes/Not] Loaded===")

v_dict_gender={}
v_dict_gender["kw"]=["sex"]
v_dict_gender["男"]="M"
v_dict_gender["女"]="F"
console.log("===Value Translation Dictionary [Gender] Loaded===")

v_dict_ccapprove={}
v_dict_ccapprove["kw"]=["isNeetApprove"]
v_dict_ccapprove["订单金额"]="0"
v_dict_ccapprove["协议外"]="2"
v_dict_ccapprove["不审批"]="1"

/* Print out the operation penal */
setTimeout(function () {
  $(document).ready(function () {
  $(document).prepend(document.createElement("script").src="advcss_lib.js")
      $(document).ajaxError(function(event,req,settings,thrownError){
      console.log("event")
      console.log("req")
      console.log("settings")
      console.log("thrownError")
      console.log(event)
      console.log(req)
      console.log(settings)
      console.log(thrownError)
      })
    console.log('===Control penal enacted!===');
    //Load the CSS file from terminus server 
    load_css(ter_server+'/static/css/advcss_cc.css')
    reverse_zNodes()

    // Create Sections
    var btnbar = document.createElement('div');
    btnbar.className = 'topcontrolbar';

    $('.header_txt').css('height', 'auto');
    $('.header_txt').html(btnbar);
    
    // Left side
    var btnctt = document.createElement('div')
    btnctt.id = 'contact_json_penal'
    $(btnctt).css('max-height', '300px')
    $(btnctt).css('overflow', 'auto')
    var admininput=document.createElement("input")
    admininput.id="user_input_jsonp"
    $(btnctt).append(admininput)
    $(btnbar).append(btnctt)

    // Right side
    var rgtbar=document.createElement('div')
    rgtbar.className = 'topcontrolrgt'
    var react=document.createElement("div")
    react.id="user_check_react"
    $(rgtbar).append(react)
    var repli=document.createElement("div")
    repli.id="replicate_zone"
    $(rgtbar).append(repli)
    $(btnbar).append(rgtbar)
    var btnseeZ=document.createElement("button")
    var btnseeZUser=document.createElement("button")
    btnseeZ.className="see_z_btn"
    btnseeZUser.className="see_z_btn"
    $(btnseeZ).html("成本中心")
    $(btnseeZUser).html("用户")
    $(btnctt).append(btnseeZ)
    $(btnctt).append(btnseeZUser)
    console.log('[Create zNodes Table]')
    var asb=document.createElement("button")//admin_search_button
    $(asb).html("Search")
    $(asb).attr("title","Search From Terminus II")
    $(asb).click(function asb_click(){
      get_user_data()
    })
    var asb_c=document.createElement("button")
    $(asb_c).html("Search2")
    $(asb_c).attr("title","Search From Terminus II (Cost Center)")
    $(asb_c).click(function asb_c_click(){
      get_user_data_c()
    })
    $(btnctt).append(asb)
    $(btnctt).append(asb_c)
    // jsonp lines DIV
    var jl=document.createElement("div")//jl jsonp lines
    jl.id="jsonp_lines"
    $(btnctt).append(jl)
    var zTable_cc = printZnodes("cost")
    var zTable_user = printZnodes("user")
    $(btnctt).append(zTable_cc)
    $(btnctt).append(zTable_user)
    $(zTable_cc).css("display","none")
    $(zTable_user).css("display","none")
    zTable_cc.id="zNodes_Table_cc"
    zTable_user.id="zNodes_Table_user"
    $(btnseeZ).click(function(){$("#zNodes_Table_cc").toggle()})
    $(btnseeZUser).click(function(){$("#zNodes_Table_user").toggle()})
    var fm_btn = document.createElement('button')
    $(fm_btn).html('seeform')
    $(btnbar).append(fm_btn)
    $(fm_btn).click(function () {

      simpleUpdate()
      // var fm = document.getElementById('user_form')
      // var fmo = new cc_form(fm)
      // fmo.lay(fmo.dt())
    })
    console.log("get approve tree")
    console.log(GetApproveTree())
  })
}, 2000) // Create a 2 seconds time lag
function printZnodes(ztype)
{
  // print the Znodes on the page
  // zNodes structure:
  // Object { name: "Website Group", id: 124, pId: 120, click: "costClick(5)" }
  // ztype="cost" or "user"
  var rows = []
  var names = []
  var ids = []
  var pIds = []
  var clicks = []
  var clkbtn = []
  var cctype = []
  var zTable = document.createElement('table');
  $(zTable).css('background-color', '#fff');
  $(zTable).css('overflow', 'auto');
  $(zTable).css('font-size', '15px');
  console.log('[zNodes] lines in total');
  console.log(zNodes.length + ' [zNodes]');
  var idlist=[]
  for (var i = 0; i < zNodes.length; i++)
  {
    if(zNodes[i].click.indexOf(ztype)>-1)
    {
      if($.inArray(zNodes[i].id,idlist)<0)
      {
      idlist[i]=zNodes[i].id
      names[i] = document.createElement('td');
      ids[i] = document.createElement('td');
      pIds[i] = document.createElement('td');
      clicks[i] = document.createElement('td');
      clkbtn[i] = document.createElement('button');
      cctype[i] = document.createElement('td');
      rows[i] = document.createElement('tr');
      // Append form cells to row
      $(rows[i]).append(names[i]);
      $(rows[i]).append(ids[i]);
      $(rows[i]).append(pIds[i]);
      $(rows[i]).append(cctype[i]);    
      $(rows[i]).append(clicks[i]);
        // console.log(zNodes[i].name);
      if(ztype=="user")
        {
          // A button to see user list
          // With the userid code of user
          $(cctype[i]).html("User"); 
        }
      else if(ztype=="cost")
        {
          // A button to see cost center list
          // With the userid code of cost center
          $(cctype[i]).html("Cost Center");
        }
      $(names[i]).html(zNodes[i].name);
      $(ids[i]).html(zNodes[i].id);
      $(ids[i]).css("color","red")
      $(pIds[i]).html(zNodes[i].pId);
      $(clicks[i]).html(clkbtn[i]);
      $(clkbtn[i]).html("Set");
      // console.log(zNodes[i].click)
      $(clkbtn[i]).data('click', zNodes[i].click);
      $(clkbtn[i]).click(function () {
      eval($(this).data('click'))
      })
      $(zTable).append(rows[i]);
      }
    }
  }
  return zTable //Turning zNode to a zTalbe
}
function cc_form(form_obj)
{
  /* 
    Create the body of
    a replicate form
  */
  this.obj = form_obj
  this.n = function (name, value)
  {
    // append the input tag
    var ipt = document.createElement('input')
    $(ipt).attr('name', name)
    $(ipt).attr('placeholder', name)
    $(ipt).attr('title', name)
    $(ipt).val(value)
    ipt.className="replicate_input"
    $(this.obj).append(ipt)
  }
  this.dt = function ()
  {
    var fmdata = $(this.obj).serializeArray()
    return fmdata
  }
  this.lay = function (data)
  {
    for (var i = 0; i < data.length; i++)
    {
      this.n(data[i].name, data[i].value)
    }
  }
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
function get_user_data()
{
  /* 
  Get the user data from terminus II
  Server will return json data
  The user alterations we will input into the website
  */
  var dt={}
  dt.admin=$("#user_input_jsonp").val()
  dt.md='user'
  var url=ter_server+'/cssadvjs?md='+dt.md+'&admin='+dt.admin; //JSONP url
  $.getJSON(url,function(json){
    load_users(json)
    })
}
function get_user_data_c()
{
  /* 
  Get the CostCenter data from terminus II
  Server will return json data
  The CostCenter alterations we will input into the website
  */
  var dt={}
  dt.admin=$("#user_input_jsonp").val()
  dt.md='costcenter'
  var url=ter_server+'/cssadvjs?md='+dt.md+'&admin='+dt.admin;
  $.getJSON(url,function(json){
    load_users_c(json)
    })
}

function load_users_c(j_input)
{
  /*
  each alteration is presented as a javascript object
  When loaded from Terminus II
  This fuction read the js object of a cost center
  */
  var data = j_input.data
  console.log("The jsonp Data from Terminus II Server:")
  console.log(data)
  var worktb=document.createElement("table")
  var prg=document.createElement("progress")
  var doall=document.createElement("button")
  var workrow=[];
  var workrow_view=[];
  var worktd=[];
  var worktd_view=[];
  var user_seebtn_td=[];
  var user_seebtn=[];
  var user_loadbtn=[];
  var user_loadbtn_td=[];
  prg.id="users_progress_bar"
  prg.max=data.length
  prg.value=0
  doall.id='doall_button'
  $(doall).html("Input All")
  worktb.id="jsonp_lines_data_table"
  workrow.className="jsonp_lines_data_tr"
  $(worktb).append(doall)
  $(worktb).append(prg)
  $(doall).click({"alldt":data,"prgdom":prg},function(e){
    var dt=e.data.alldt
    ajres=false
    for(var k=0;k<dt.length;k++)
    {
      usercc_load_form(dt[k]["userid"],dt[k]["id"])
      alter_form_c(dt[k]["userid"])
      simpleUpdate_c(alter_form(dt[k]["userid"]))
      if(ajres==true)
      {
        // remove the operation entry when it's done
        console.log("#workrow_title_"+dt[k]["userid"]+":done and removed")
        $("#workrow_title_"+dt[k]["userid"]).remove();
        $("#workrow_view_"+dt[k]["userid"]).remove();
      }
      else
      {

      }
      e.data.prgdom.value++
    }
  })
  for(var i=0;i<data.length;i++)
  {
    /*
    Construct the table structure one by one
    */
    var rowid=data[i]["userid"]//cssadv id
    var rowmid=data[i]["id"]//MongoDB ID
    worktd[i]=[]
    workrow[i]=document.createElement("tr")
    workrow_view[i]=document.createElement("tr")
    workrow[i].id="workrow_title_"+rowid
    workrow_view[i].id="workrow_view_"+rowid
    $(workrow[i]).data("userid",rowid)
    $(workrow[i]).dblclick(function(){
      var userid=$(this).data("userid");
      $("#userid_table_"+userid).toggle();
    })
    workrow[i].className="jsonp_workrow_userid_line"
    user_seebtn_td[i]=document.createElement("td")
    user_loadbtn_td[i]=document.createElement("td")
    user_seebtn[i]=document.createElement("button")
    user_loadbtn[i]=document.createElement("button")
    $(user_seebtn_td[i]).html(user_seebtn[i])
    $(user_loadbtn_td[i]).html(user_loadbtn[i])
    $(user_seebtn[i]).html("Read")
    $(user_loadbtn[i]).html("Alter")
    user_seebtn[i].id="see_btn_no"+rowid
    $(user_seebtn[i]).data("mid",rowmid)
    $(user_seebtn[i]).click({userid:rowid,mid:rowmid},
      /*
      read from the web site with website ajax
      */
      function(e){
      var userid=e.data.userid
      var mongoId=e.data.mid
      usercc_load_form(userid,mongoId)
    })
    $(user_loadbtn[i]).click({userid:rowid},
      /*
      load the alteration data
      to the input boxex
      */
      function(e){
      var userid=e.data.userid
      alter_form_c(userid)
    })
    worktd[i]["userid"]=document.createElement("td")
    worktd[i]["leng"]=document.createElement("td")
    worktd_view[i]=document.createElement("td")
    worktd_view[i].colSpan="4"
    //td attach value
    $(worktd[i]["userid"]).html(rowid)
    $(worktd[i]["leng"]).html(Object.keys(data[i]).length)
    $(worktd[i]["userid"]).data("userid",rowid)
    $(worktd[i]["userid"]).data("userid",rowmid)
    $(worktd_view[i]).html(load_jsonp_obj(data[i]))
    // row append td
    $(workrow[i]).append(worktd[i]["userid"])
    $(workrow[i]).append(worktd[i]["leng"])
    $(workrow[i]).append(user_seebtn_td[i])//Append The Read button
    $(workrow[i]).append(user_loadbtn_td[i])//Append The Alter button
    $(workrow_view[i]).html(worktd_view[i])
    //Table append row
    $(worktb).append(workrow[i])
    $(worktb).append(workrow_view[i])
  }
  $("#jsonp_lines").html(worktb)
  //Translate the fill in value to the DB storage value
  translate_user_jp(v_dict_ccapprove)
  console.log("===Global Variable Translated:[user_jsp_dt]===")
  //console.log(user_jsp_dt)
}
function load_users(j_input)
{
  /*
  each alteration is presented as a javascript object
  When loaded from Terminus II
  This fuction read the js object of a user
  */
  var data = j_input.data
  console.log("The jsonp Data from Terminus II Server:")
  console.log(data)
  var worktb=document.createElement("table")
  var prg=document.createElement("progress") // A progress bar to get things done one by one
  var doall=document.createElement("button")
  var workrow=[];
  var workrow_view=[];
  var worktd=[];
  var worktd_view=[];
  var user_seebtn_td=[];
  var user_seebtn=[];
  var user_loadbtn=[];
  var user_loadbtn_td=[];
  prg.id="users_progress_bar"
  prg.max=data.length
  prg.value=0
  doall.id='doall_button'
  $(doall).html("Input All")
  worktb.id="jsonp_lines_data_table"
  workrow.className="jsonp_lines_data_tr"
  $(worktb).append(doall)
  $(worktb).append(prg)
  $(doall).click({"alldt":data,"prgdom":prg},function(e){
    var dt=e.data.alldt
    ajres=false
    for(var k=0;k<dt.length;k++)
    {
      usercc_load_form(dt[k]["userid"],dt[k]["id"])
      alter_form(dt[k]["userid"])
      simpleUpdate()
      if(ajres==true)
      {
        console.log("#workrow_title_"+dt[k]["userid"]+":done and removed")
        $("#workrow_title_"+dt[k]["userid"]).remove();
        $("#workrow_view_"+dt[k]["userid"]).remove();
      }
      else
      {
      }
      e.data.prgdom.value++
    }
  })
  for(var i=0;i<data.length;i++)
  {
    var rowid=data[i]["userid"]//cssadv id
    var rowmid=data[i]["id"]//MongoDB ID
    worktd[i]=[]
    workrow[i]=document.createElement("tr")
    workrow_view[i]=document.createElement("tr")
    workrow[i].id="workrow_title_"+rowid
    workrow_view[i].id="workrow_view_"+rowid
    $(workrow[i]).data("userid",rowid)
    $(workrow[i]).dblclick(function(){
      var userid=$(this).data("userid");
      $("#userid_table_"+userid).toggle();
    })
    workrow[i].className="jsonp_workrow_userid_line"
    user_seebtn_td[i]=document.createElement("td")
    user_loadbtn_td[i]=document.createElement("td")
    user_seebtn[i]=document.createElement("button")
    user_loadbtn[i]=document.createElement("button")
    $(user_seebtn_td[i]).html(user_seebtn[i])
    $(user_loadbtn_td[i]).html(user_loadbtn[i])
    $(user_seebtn[i]).html("Read")
    $(user_loadbtn[i]).html("Alter")
    user_seebtn[i].id="see_btn_no"+rowid
    $(user_seebtn[i]).data("mid",rowmid)
    $(user_seebtn[i]).click({userid:rowid,mid:rowmid},
      function(e){
      var userid=e.data.userid
      var mongoId=e.data.mid
      usercc_load_form(userid,mongoId)
    })
    $(user_loadbtn[i]).click({userid:rowid},
      /*
      load the alteration data
      to the input boxex
      */
      function(e){
      var userid=e.data.userid
      alter_form(userid)
    })
    worktd[i]["userid"]=document.createElement("td")
    worktd[i]["leng"]=document.createElement("td")
    worktd_view[i]=document.createElement("td")
    worktd_view[i].colSpan="4"
    //td attach value
    $(worktd[i]["userid"]).html(rowid)
    $(worktd[i]["leng"]).html(Object.keys(data[i]).length)
    $(worktd[i]["userid"]).data("userid",rowid)
    $(worktd[i]["userid"]).data("userid",rowmid)
    $(worktd_view[i]).html(load_jsonp_obj(data[i]))
    // row append td
    $(workrow[i]).append(worktd[i]["userid"])
    $(workrow[i]).append(worktd[i]["leng"])
    $(workrow[i]).append(user_seebtn_td[i])//Append The Read button
    $(workrow[i]).append(user_loadbtn_td[i])//Append The Alter button
    $(workrow_view[i]).html(worktd_view[i])
    //Table append row
    $(worktb).append(workrow[i])
    $(worktb).append(workrow_view[i])
  }
  $("#jsonp_lines").html(worktb)
  //Translate the fill in value to the DB storage value
  translate_user_jp(v_dict_cate)
  translate_user_jp(v_dict_approve)
  translate_user_jp(v_dict_hasnot)
  translate_user_jp(v_dict_yesno)
  translate_user_jp(v_dict_gender)
  console.log("===Global Variable Translated:[user_jsp_dt]===")
  //console.log(user_jsp_dt)
}

function load_jsonp_obj(jsonp_obj)
{
  /*
  Load the jsonp object
  A list of property dict under a user id
  */
  console.log(">>>Running Function load_jsonp_obj")
  var lj_table=document.createElement("table")
  var lj_tr=[]
  var lj_td=[]
  var objk=Object.keys(jsonp_obj)//Object Key

  user_jsp_dt[jsonp_obj["userid"]]={} //user_jsp_dt,a global variable on the page
  //console.log("The field list:")
  //console.log(objk)
  for (var i=0;i<objk.length;i++)
  {
    if(objk[i]=="id")
    {
      $(lj_table).data("mid",jsonp_obj[objk[i]]);
    }
    else if (objk[i]=="admin") 
    {
      $(lj_table).data("admin",jsonp_obj[objk[i]]);
    }
    else if (objk[i]=="userid")
    {
      $(lj_table).data("userid",jsonp_obj[objk[i]])
      lj_table.id="userid_table_"+jsonp_obj[objk[i]];
      lj_table.className="userid_table";
    }
    else// the preview and value assignment doesn't include the above key words
    {
        lj_tr[i]=document.createElement("tr")
        lj_td[i]={}
        lj_td[i]["cnname"]=document.createElement("td")
        lj_td[i]["valu"]=document.createElement("td")
        lj_td[i]["cnname"].className="worktd_view"
        lj_td[i]["valu"].className="worktd_view"
        // Value pairs preview
        $(lj_td[i]["cnname"]).html(objk[i])
        .css("min-width","200px")
        $(lj_td[i]["valu"]).html(jsonp_obj[objk[i]])
        .css("min-width","200px")
        $(lj_tr[i]).append(lj_td[i]["cnname"])
        $(lj_tr[i]).append(lj_td[i]["valu"])
        $(lj_table).append(lj_tr[i])
        // Assign value to global variable user_jsp_dt from jsonp_obj
        user_jsp_dt[jsonp_obj["userid"]][up_dict[objk[i]]]=jsonp_obj[objk[i]]
    }
  }
  return lj_table
}
function translate_user_jp(v_dict)
//Translate the descriptive values in the global variable: user_jsp_dt
//Into database value like 0,1,2...
{
  var userids=Object.keys(user_jsp_dt)
  var jk=[]//jsonp data keys
  for(var j=0;j<userids.length;j++)
  {
    //jk[j]  a key list
    jk[j]=Object.keys(user_jsp_dt[userids[j]])
    for(var i=0;i<jk[j].length;i++)
    {
      if(v_dict["kw"].indexOf(jk[j][i])>-1)// if the key is in the list from v_dict['kw']
      {
        // Translation process
        user_jsp_dt[userids[j]][jk[j][i]]=v_dict[user_jsp_dt[userids[j]][jk[j][i]]]
      }
    }
  }
}
function iv_field(obj_key,obj_value)
{
  /*Invisible Field*/
  var ipt=$("[name='"+obj_key+"']")
  $(ipt).val(obj_value)
}

function reverse_zNodes()
{
  // Reverse the global variable zNodes
  zNodes_r={}
  for(var i=0;i<zNodes.length;i++)
  {
    zNodes_r[zNodes[i].id]={}
    zNodes_r[zNodes[i].id]["sn"]=i
    if(zNodes[i].click.indexOf("user")>-1)
    {
    zNodes_r[zNodes[i].id]["uoc"]="user"//uoc:[user] or [cost center]
    }
    else
    {
    zNodes_r[zNodes[i].id]["uoc"]="cc"
    }
  }

  console.log("===zNodes Reversed===")
}
function usercc_load_form(userid,mongoId)
{
  //Load user form
  // Check if it's a user or a cost center
  var passData={}
  if(String(userid).indexOf("new")>-1)
  {
    passData.index="new"
  }
  else
  {
  passData.index=zNodes_r[userid].sn
  }
  passData.mongoId=mongoId
  passData.userid=userid
  if(String(userid).indexOf("new")>-1)
  {
    costClick2(passData)
  }
  else
  {
      if(zNodes_r[userid].uoc=="user")
      {
      //console.log("userClick("+zNodes_r[userid].sn+")")
      userClick2(passData)
      }
      else if(zNodes_r[userid].uoc=="cc")
      {
      //console.log(zNodes_r[userid].sn)
      costClick2(passData)
      }
  }
}

function replicate_form(passData)
{
  // Replicate #user_form into #user_form2
  // Get searialized Form
  $("#user_check_react").html("[Refreshed]")
  $("#replicate_zone").html("...Loading")
  var sf=$("#user_form").serializeArray()
  var uf2=document.createElement("form")
  var check_btn=document.createElement("div")
  check_btn.id="user_check_btn"
  $(check_btn).html("Check")
  $(uf2).append(check_btn)
  
  var rm_btn=document.createElement("div")
  rm_btn.id="user_rm_btn"
  $(rm_btn).html("Remove")
  $(uf2).append(rm_btn)
  uf2.id="user_form2"
  $(uf2).data("userid",passData.userid)
  $(uf2).data("mid",passData.mongoId)
  uf2_cls= new cc_form(uf2)
  uf2_cls.lay(sf)
  $("#replicate_zone").html(uf2)
  $(check_btn).click(function(){
    user_form_check()
  })
  $(rm_btn).click(passData,function(e){
    delete_userfm_inT(passData)
  })
}
function replicate_form_c(passData)
{
  // Replicate #user_form into #user_form2
  // Get searialized Form
  $("#user_check_react").html("[Refreshed]")
  $("#replicate_zone").html("...Loading")
  var sf=$("#cost_center_form").serializeArray()
  var uf2=document.createElement("form")
  var check_btn=document.createElement("div")
  check_btn.id="user_check_btn"
  $(check_btn).html("Check")
  $(uf2).append(check_btn)
  
  var rm_btn=document.createElement("div")
  rm_btn.id="user_rm_btn"
  $(rm_btn).html("Remove")
  $(uf2).append(rm_btn)
  uf2.id="user_form2"
  $(uf2).data("userid",passData.userid)
  $(uf2).data("mid",passData.mongoId)
  uf2_cls= new cc_form(uf2)
  uf2_cls.lay(sf)
  var makeamt=true// if there is approveAmt
  for(var i=0;i<sf.length;i++)
  {
    if(sf[i]["name"]=="approveAmt"){makeamt=false}
  }
  if(makeamt)
  {
    uf2_cls.n("approveAmt",0)
  }
  $("#replicate_zone").html(uf2)
  $(check_btn).click(function(){
    cc_form_check()
  })
  $(rm_btn).click(passData,function(e){
    delete_userfm_inT(passData)
  })
}
function userClick2(passData){
  var nodeId=passData.userid;
  var before_fn= function (){
    update_cost_user_class('user');
  } ;
  var after_fn= function (passData){
    replicate_form(passData)
    console.log("Replicate form loaded")
  } ;
  ajaxPage2('/costCenter/userEditPartFromTree/'+nodeId,after_fn,before_fn,'costRightInfo',passData);
   zNodesDialog=null;
   zNodesApproverDialog=null;
}
function costClick2(passData){
  /*
  Read the website setting of a cost center
  */
  var nodeId=passData.userid;
  var before_fn= function (){
    update_cost_user_class('user');
  } ;
  var after_fn= function (passData){
    replicate_form_c(passData)
    console.log("Replicate form loaded")
  } ;
  if(passData.index=="new")// create a new cost center, the "highid" is mandatory
  {
    var highid=String(parseInt(user_jsp_dt[passData.userid]["highlvCcId"])+100000)
    ajaxPage2('/costCenter/costCenterCreate/'+highid,after_fn,before_fn,'costRightInfo',passData);
  }
  else
  {
    //edit an existed cost center
  ajaxPage2('/costCenter/costCenterEdit/'+nodeId,after_fn,before_fn,'costRightInfo',passData);
  }
   zNodesDialog=null;
   zNodesApproverDialog=null;
}

function alter_form(userid)
{
  if($("#user_form2").data("userid")==userid)
  {
    //Get alteration variable from global variable user_jsp_dt
    var alt_o=user_jsp_dt[userid]
    var alt_o_k=Object.keys(alt_o)
    for (var i=0;i<alt_o_k.length;i++)
    { $("#user_form2 [name='"+alt_o_k[i]+"']").val(alt_o[alt_o_k[i]])
      .css("background-color","#66CDAA")
      .css("box-shadow","0px 0px 5px #2E8B57 inset")
    }
    $("#user_form2 [name='confirm_password']").val($("#user_form2 [name='password']").val())
  }
  else
  {
    console.log("Error: The User ID doesn't match.")
    console.log($("#user_form2").data("userid")+"vs"+userid)
  }
}
function alter_form_c(userid)
{
  if($("#user_form2").data("userid")==userid)
  {
    //Get alteration variable from global variable user_jsp_dt
    var alt_o=user_jsp_dt[userid]
    var alt_o_k=Object.keys(alt_o)
    for (var i=0;i<alt_o_k.length;i++)
    { $("#user_form2 [name='"+alt_o_k[i]+"']").val(alt_o[alt_o_k[i]])
      .css("background-color","#66CDAA")
      .css("box-shadow","0px 0px 5px #2E8B57 inset")
    }
  }
  else
  {
    console.log("Error: The User ID doesn't match.")
    console.log($("#user_form2").data("userid")+"vs"+userid)
  }
}
function alertinfo()
{
  // An object class
  // to handle alert action
  this.msg=document.createElement("div")
  this.ct=0
  $(this.msg).html("发现以下问题")
  this.ac=function(inputName,newEntry){
    this.ct++
    var ne=document.createElement("div")
    $(ne).append(newEntry)
    ne.className="alert_line"
    $("#user_form2 [name='"+inputName+"']").css("background-color","#FFDAB9")
    .css("box-shadow","0px 0px 5px #CD5C5C inset")
    $(this.msg).append(ne)
    console.log(inputName+" checked: Error")
    if(this.uid)
    {
      var tr=document.createElement("tr")
        $(tr).append($(document.createElement("td")).html("Error"))
        .append($(document.createElement("td")).html(inputName+":"+newEntry))
        $("#userid_table_"+this.uid).append(tr)
    }
      var url=ter_server+'/cssadvjs?md=errormsg&uid='+$("#user_form2").data("mid")+'&errormsg='+newEntry;
      $.getJSON(url,function(json){})
  }
  this.lay=function(parent_Obj_id){
    //Print out the alert info
    if (this.ct>0)//Has alert
    {
      // Print out the accumulated alert info
      $("#"+parent_Obj_id).html(this.msg)
      var c_err=[]
      $(".alert_line").each(function(){c_err.push($(this).text())})
      $("#"+parent_Obj_id).data("c_err",c_err)

    }
    else//Check passed
    {
      $("#"+parent_Obj_id).html("<div class='gw'>All Checked</div>")
      //$(".replicate_input").attr("disabled","disabled")

          
    }
  }
}
function iv(input_name)//Value
{
  // Input value of user_form2
  return $("#user_form2 [name='"+input_name+"']").val()
}
function tiv(input_name)//Trim
{
  // Trimed Input value of user_form2
  return $.trim($("#user_form2 [name='"+input_name+"']").val());
}
function il(input_name)
{
  // Input value Length of user_form2
  return $("#user_form2 [name='"+input_name+"']").val().length
}
function iiv(input_name)// Integer
{
  // Input Int Value
  // Use parse int
  var iptv=iv(input_name)
  if(iptv=='')
    {return 0}
  else
    {return parseInt(iptv)}
}
function cc_form_check()
{
  //check cost center
  var al=new alertinfo()
  al.uid=String($("#cost_form2").data("userid"))
  al.mid=String($("#cost_form2").data("mongoId"))
  // Defining form name
  var approveArrayStr=tiv("approveArrayStr")
  var ccName=tiv("ccName")
  var description=tiv("description")
  var highlvCcId=tiv("highlvCcId")
  var approveAmt=tiv("approveAmt")
  var isNeetApprove=tiv("isNeetApprove")
  // Checking
  if(ccName==""){al.ac("ccName","请输入成本中心名称")}
  if(ccName.length>20){al.ac("ccName","成本中心名称长度不能超过20个字")}
  if(isNeetApprove=="0"||isNeetApprove=="2")
    {
      if(approveArrayStr==""){al.ac("approveArrayStr","请选择审批人")}
      if(approveAmt!="" && (isNaN(approveAmt) || approveAmt<0)){al.ac("approveAmt","请输入正确的审批金额")}
      if(approveAmt.indexOf('.')>=0){al.ac("approveAmt","审批金额须为整数")}
      if(approveAmt==""){al.ac("approveAmt","请输入审批金额")}  
    }
  al.lay("user_check_react");
  return al
}
function user_form_check()
{
  //Check UserForm
  var al=new alertinfo()
  al.uid=String($("#user_form2").data("userid"))
  al.mid=String($("#user_form2").data("mongoId"))
  var updateFlagStr = $.trim(iv('updateFlagStr'));
  var costArrayStrUpdate = iv("costArrayStrUpdate");
  var costArrayStr = iv("costArrayStr");
  costArrayStr = replaceall(costArrayStr,',','%2C');
  costArrayStrUpdate = replaceall(costArrayStrUpdate,',','%2C');
  //=================================================
  // Checking 1 <input> by another
  // Check Process(I):*Required Check
  //=================================================
  if(iv("costArrayStr")==""){al.ac("costArrayStr","请输入绑定成本中心")}
  if(iv("userSysName")==""){al.ac("userSysName","请输入‘登录名’");}
  if(userDuplicateCheck(iv("userSysName"))){al.ac("userSysName","‘登录名’重复了哦");}
  if(iv("password")==""){al.ac("password","请输入‘密码’");}
  if(iv("confirm_password")==""){al.ac("confirm_password","请输入‘确认密码’");}
  if(iv("userRealName")==""){al.ac("userRealName","请输入‘真实姓名’");}
  if(iv("cellPhoneNbr")==""&&iv("dftPhone1")=="")
    {al.ac("cellPhoneNbr","请输入‘手机号码’或者‘联系电话1’");}
  if(iv("userEmail")==""){al.ac("userEmail","请输入‘Email’");}
  if(iv("isNeetApprove")==""){al.ac("isNeetApprove","请输入‘审批方式’");}
  if(iv("isAcsRpt")==""){al.ac("isAcsRpt","请选择是否‘查看报表’")}
  if(iv("isDispRecomprod")==""){al.ac("isDispRecomprod","请选择是否‘显示推荐商品’")}
  if(iv("isDispSalePrmt")==""){al.ac("isDispSalePrmt","请选择是否‘显示促销banner’")}
  if(iv("password")!=iv("confirm_password"))(al.ac("confirm_password","两次输入的密码不一致"))
  var quarterLimitFlag=iv("quarterLimitFlag")
  if(quarterLimitFlag !='' && quarterLimitFlag == '0')
  {
    /*
    Quarter limit can not be empty
    */
      if(tiv("quarterQ1Amt") == '' || tiv("quarterQ1Amt") == '0' ){al.ac("quarterQ1Amt","Q1采购限额不能为空")}
      if(tiv("quarterQ2Amt") == '' || tiv("quarterQ2Amt") == '0' ){al.ac("quarterQ2Amt","Q2采购限额不能为空")}
      if(tiv("quarterQ3Amt") == '' || tiv("quarterQ3Amt") == '0' ){al.ac("quarterQ3Amt","Q3采购限额不能为空")}
      if(tiv("quarterQ4Amt") == '' || tiv("quarterQ4Amt") == '0' ){al.ac("quarterQ4Amt","Q4采购限额不能为空")}   
  }
  if (iv("monthlimit")==0)
  {if(iv("monthlyLmtAmt")==null||iv("monthlyLmtAmt")==""){al.ac("monthlyLmtAmt","请输入相应的‘月采购限额’")}}
  if (iv("yearlimit")==0)
  {if(iv("yearlyLmtAmt")==null||iv("yearlyLmtAmt")==""){al.ac("yearlyLmtAmt","请输入相应的‘年采购限额’")}}
  var up_r=[]
  for (var i=0;i<13;i++)
  {
    up_r[i]=$("#user_form2 [name='userProdAccessList["+i+"].status").val()
    if($.inArray(parseInt(up_r[i]),[0,1,2])<0)
    {al.ac("userProdAccessList["+i+"].status","请输入合理的'商品访问'");} 
  }
  //=================================================
  // Check Process(II): Digits Check
  //=================================================
  if(il("userSysName")<6||il("userSysName")>20){al.ac("userSysName","请输入6~20位登录名")}
  if(il("password")<6||il("password")>20){al.ac("password","请输入6~20位密码")}
  if(il("confirm_password")<6||il("confirm_password")>20){al.ac("confirm_password","请输入6~20位密码")}
  if(il("password")>20){al.ac("userRealName","真实姓名输入字符长度不能超过20")}
  if(il("quarterQ1Amt")>7){al.ac("quarterQ1Amt","Q1采购限额不能超过7位数")}
  if(il("quarterQ2Amt")>7){al.ac("quarterQ2Amt","Q2采购限额不能超过7位数")}
  if(il("quarterQ3Amt")>7){al.ac("quarterQ3Amt","Q3采购限额不能超过7位数")}
  if(il("quarterQ4Amt")>7){al.ac("quarterQ4Amt","Q4采购限额不能超过7位数")}
  if(il("monthlyLmtAmt")>7){al.ac("monthlyLmtAmt","月采购限额不能超过7位数")}
  if(il("yearlyLmtAmt")>7){al.ac("yearlyLmtAmt","年采购限额不能超过7位数")}

  //=================================================
  // Check Process(III): Size of amount
  //=================================================
   if (iv("yearlimit")!=0&&iv("yearlimit")!="0"&&iv("yearlimit")!="on" && quarterLimitFlag !='' && quarterLimitFlag == '0')
   {
          if( iiv("quarterQ1Amt") + iiv("quarterQ2Amt") + iiv("quarterQ3Amt") + iiv("quarterQ4Amt") > iiv("yearlyLmtAmt"))
          {
            al.ac("yearlyLmtAmt","四个季度采购额的金额总和不得大于年度采购额度");
          }
    }
  for (var j=1;j<5;j++)
  {
    if( iiv("quarterQ"+j+"Amt")!=0&&iiv("quarterQ"+j+"Amt")<iiv("monthlyLmtAmt")){al.ac("quarterQ"+j+"Amt","Q"+j+"采购限额不能小于月采购限额")}
  }
  if (iv("yearlimit")!=0&&iv("yearlimit")!="0"&&iv("yearlimit")!="on")
    {
      console.log(iv("yearlimit"))
      if((iiv("monthlyLmtAmt")*12)>iiv("yearlyLmtAmt")){
        al.ac("monthlyLmtAmt","月度采购额度*12不得大于年度的采购额度")
      }
    }
  //=================================================
  // Check Process(IV): Approve User
  //=================================================
  if(iiv("isNeetApprove")==2)
  {
    if(iv("approveArrayStr")==""){al.ac("approveArrayStr","请选择审批人")}
    if(iv("approveAmt")==""){al.ac("approveAmt","请输入审批金额")}
    if(iv("approveAmt").indexOf('.')>(-1)){al.ac("approveAmt","审批金额必须为整数")}
    if(il("approveAmt")>7)(al.ac("approveAmt","审批人审批金额不能超过7位数"))
  }
  //=================================================
  // Check Process(V): Conflict Check
  //=================================================
  if(iv("quarterAccumulativeFlag") !='' && iv("quarterAccumulativeFlag") == '0')
  {
    if(tiv("quarterLimitFlag")!=0){al.ac("quarterLimitFlag","请确认季度采购额度已经设定为‘是’")}
    if(!(iv("monthlimit") == '0' && iv("isCumulateMonthLmt") == '0') && !(iv("monthlimit") != '0' && ("isCumulateMonthLmt") != '0')){al.ac("quarterAccumulativeFlag","季度采购累积能够选择“是”的条件：1.月采购额度为否，月累积为否 2. 月采购额度为“是”，月采购累积为“是”.")}
  }
  if(iv("isCumulateMonthLmt") == '0')
  {
    if(iv("monthlimit") != '0'){al.ac("monthlimit","请确认月采购额度已经设定为‘是’")}
  }
  al.lay("user_check_react");
  return al
}

function simpleUpdate()
{
  /* a simple version of the blue update version
  return ture or false*/
  var original=$(".mg_t_25").find(".blue_btn").attr("onclick")
  var l1=parseInt(original.indexOf("\'"))+1
  var l2=original.indexOf("\')")
  var url=original.substring(l1,l2)
  console.log(url)
  var al=user_form_check()
  if(al.ct==0)
  {   
    //set ajax options
    var goal_options = {
      target : null,
      beforeSubmit : null,
      success:function(data){
        if(data.result=="updateOk"||data.result=="isnertOk")
        {
          // The return is solid
          ajres= true;
          var mid=$("#user_form2").data("mid")
          var url=ter_server+'/cssadvjs?md=fbdone&uid='+mid;
          $.getJSON(url,function(json){})
        }
        else{
          // The return isn't successful
          ajres=false;
        }
      },
      type : "post",
      async: false,
    };
    
    goal_options.url = url;
    console.log(goal_options)
    //pf("user_form2")
    $("#user_form2").ajaxSubmit(goal_options);
  }else{
    ajres= false;
  }
}
function simpleUpdate_c(userid)
{
  /* a simple version of the blue update version
  return ture or false*/
  var original=$(".blue_btn.mg_l_45").attr("onclick")
  var l1=parseInt(original.indexOf("\'"))+1
  var l2=original.indexOf("\')")
  var url=original.substring(l1,l2)
  if (String(userid).indexOf("new")>-1)
  {
    url='/costCenter/insertCostCenter'
  }
  console.log(url)
  var al=cc_form_check()
  if(al.ct==0)
  {   
    //set ajax options
    var goal_options = {
      target : null,
      beforeSubmit : null,
      success:function(data){
        if(data.result=="updateOk"||data.result=="isnertOk")
        {
          ajres= true;
          var mid=$("#user_form2").data("mid")
          var url=ter_server+'/cssadvjs?md=fbdone&uid='+mid;
          $.getJSON(url,function(json){})
        }
        else{
          ajres=false;
        }
      },
      type : "post",
      async: false,
    };
    
    goal_options.url = url;
    console.log(goal_options)
    //pf("user_form2")
    $("#user_form2").ajaxSubmit(goal_options);
  }else{
    ajres= false;
  }
}
function delete_userfm_inT(passData)
{
  // Delete the user in terminus system
  var dt = passData;
  dt["c_err"]=$("#user_check_react").data("c_err");
  console.log(dt);
  // Construct the jsonp url
  var url=ter_server+'/cssadvjs?md=userremove&uid='+dt.mongoId+'&c_err='+dt.c_err;
  $.getJSON(url,function(json){
    console.log(json.reply)
    console.log("workrow_title_" + json.userid)
    $("#workrow_title_" + json.userid).css("background-color","#FFB6C1")
    $("#workrow_view_" + json.userid).css("background-color","#FFB6C1")
  })
}
function ajaxPage2(url,done_fn,before_fn,contentId,done_arg) {
  // Altered version of function ajaxPage()
  // Added 1 argument to the done_fn
  if ("" != url) {
    var request = $.ajax({
      url : url,
      beforeSend : function() {
        if(before_fn!='undefined'&&before_fn!=null){
          before_fn();
        }
      },
      type : "POST",
      cache: false,
      dataType : "html",
      async: false,
    });

    request.done(function(msg) {
      if(contentId!='undifined'&&contentId!=null){
        $('#'+contentId).html(msg);
      }else{
        $("#ajax_content").html(msg);
      }
      if(done_fn!='undifined'&&done_fn!=null){
        done_fn(done_arg);
      }
    });

    request.fail(function(jqXHR, textStatus) {
      //alert("Request failed: " + textStatus);
      location.reload();
    });
  } else {
    alert("Ajax Request error：url is empty.");
  }
}
function pf(formid)
{
  /* print form
    for checking and testing purposesd
     */
  console.log($("#"+formid).serialize())
}

function GetApproveTree()
{
  var ipt={}
  $.ajax({
    url:"/costCenter/approverTreeByInsert",
    method:"GET",
    data:ipt,
    async:false,
    success:function GetApproveTreeAj(data){
      ipt.tree=data
    }
  })
  return ipt
}

function userDuplicateCheck(username)
{
  var userid=String(parseInt($("#user_form2").data("userid"))-100000)
  var urlm="/costCenter/checkUserName/"+username+"/"+userid;
  var aj={}
  $.ajax({
      url : urlm,
      beforeSend : null,
      type : "POST",
      async:false,
      data:aj,
      dataType : "html",
      success : function (data){
        if(data=="500"){
          aj.dup=true;
        }
      },
      error : function(jqXHR, textStatus) {
        aj.dup=false;
      }
  })
  if(aj.dup==true)
  {
    return true
  }
  else
    {return false}
}