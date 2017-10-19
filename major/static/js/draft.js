// Before Function, After Function


function userClick2(index){
	var nodeId=zNodes[index].id;
	var before_fn= function (){
		update_cost_user_class('user');
	} ;
	var after_fn= function (){
		console.log($("#user_form").html())
	}
	ajaxPage('/costCenter/userEditPartFromTree/'+nodeId,after_fn,before_fn,'costRightInfo');
	 zNodesDialog=null;
	 zNodesApproverDialog=null;
}


function update_cost_user_class(u_type){
	// Change the class on some of the page tags
	if(u_type=='cost'){
		 $("#costRightInfo").attr("class","cost_right_info");
		 $("#cost_left_tree_id").attr("class","cost_left_tree over_f_s");
		 $("#tree_topbg_id").attr("class","tree_topbg");
	}else if(u_type=='user'){
		 $("#costRightInfo").attr("class","user_detail_info");
		 $("#cost_left_tree_id").attr("class","cost_left_tree over_f_s mg_r_15");
		 $("#tree_topbg_id").attr("class","tree_topbg pd_t_15");
	}
}

function updateOrSaveUser3(url) {
	var new_user_form_data=$('#user_form').serialize()
	if(user_form_data==new_user_form_data){
		commonAlert("用户信息未修改");
		return false;
	}
	var updateFlagStr = $.trim($('#updateFlagStr').val());
	var costArrayStrUpdate = $("#costArrayStrUpdate").val();
	var costArrayStr = $("#costArrayStr").val();
	costArrayStr = replaceall(costArrayStr,',','%2C');
	costArrayStrUpdate = replaceall(costArrayStrUpdate,',','%2C');
	if(new_user_form_data!=user_form_data && new_user_form_data.replace(costArrayStr,'')==user_form_data.replace(costArrayStrUpdate,'')){
		$('#updateFlagStr').val(0);
	}
	
	var msg = "请填写完整信息 ";
	var count=0;

	if($("#userSysName").val()==""){
		commonAlert("请输入‘登录名’");
		count++;
		return;
	}
	
	if($("#password").val()==""){
		commonAlert("请输入密码");
		count++;
		return;
	}
	
	if($("#password").val().length < 6 || $("#password").val().length > 20){
		commonAlert("请输入密码6~20位!");
		count++;
		return;
	}
	
	if($("#confirm_password").val()==""){
		commonAlert("请输入确认密码");
		count++;
		return;
	}
	if($("#confirm_password").val().length < 6 || $("#confirm_password").val

			().length > 20){
					commonAlert("请输入确认密码6~20位!");
					count++;
					return;
				}
	
	if($("#password").val()!=$("#confirm_password").val()){
		commonAlert("两次输入的密码不一致");
		count++;
		return;
	}
	
	if($("#userRealName").val()==""){
		commonAlert("请输入‘真实姓名’");
		count++;
		return;
	}
	
	if($("#userRealName").val().length>20){
		commonAlert("真实姓名输入字符长度不能超过20 !");
		count++;
		return;
	}
	
	if(count==0){
		count++;
	}else{
		count=0;
	}
	
	if($("#cellPhoneNbr").val()=="" && $("#dftPhone1").val()==""){
		commonAlert("请输入‘手机号码’或者‘联系电话1’");
		count++;
		return;
	}
	
	if($("#userEmail").val()==""){
		commonAlert("请输入邮箱");
		count++;
		return;
	}
	
	var costAry = $("#selectContent").find("a");
	if(costAry.length==0){
		commonAlert("请选择‘成本中心’");
		return;
	}
	/*
	if($.trim($("#city_name").val())==""){
		commonAlert("请选择‘配送城市’");
		return;
	}*/
	
	if($.trim($("#select_escalades").val())==""){
		commonAlert("请选择‘结算单位’");
		return;
	}
	
	$("#viewProdStyle").find("input[type='radio']").each(function(){
		if(this.checked){
			count++;
		}
	});
//	if(count==0){
//		commonAlert("请选择‘商品访问级别’");
//		return;
//	}else{
//		count=0;
//		$("#topCategory").find("input[type='checkbox']").each(function(){
//			if(this.checked){
//				count++;
//			}
//		});
//		if(count==0){
//			commonAlert("请选择‘商品访问范围’");
//			return;
//		}else{
//			count=0;
//		}
//	}
	
	$("#need_approve").find("input[type='radio']").each(function(){
		if(this.checked){
			count++;
		}
	});
	if(count==0){
		commonAlert("请选择‘是否需要审批’");
		return;
	}else{
		count=0;
	}
	
	var approveArrayStr = $.trim($('#approveArrayStr').val());
	var approveAmt = $.trim($('#approveAmt').val());
	var approveType = $.trim($('#need_approve input:checked').val())
	if(approveType==2){
		if(approveArrayStr==''){
			commonAlert("请选择审批人!");
			return false;
		}
		if(approveAmt==''){
			commonAlert("请输入审批金额!");
			return false;
		}
		if(approveAmt.indexOf('.')>=0){
			commonAlert("审批金额必须为整数!");
			return false;
		}
		if(approveAmt.length>7){
			commonAlert("审批金额不能超过7位数!");
			return false;
		}
	}
	
	var yearlyLmtAmt = $.trim($("#yearlyLmtAmtTxt").val());
	var monthlyLmtAmt = $.trim($("#monthlyLmtAmtTxt").val());

    var quarterQ1Amt = $.trim($("#quarterQ1Amt").val());
    var quarterQ2Amt = $.trim($("#quarterQ2Amt").val());
    var quarterQ3Amt = $.trim($("#quarterQ3Amt").val());
    var quarterQ4Amt = $.trim($("#quarterQ4Amt").val());

    var quarterAccumulativeFlag  = $("input[name='quarterAccumulativeFlag']:checked").val();
    var quarterLimitFlag = $.trim($('#quarterLimitFlagChoose').val());
    var monthlimit =  $("input[name='monthlimit']:checked").val();
    var isCumulateMonthLmt = $("input[name='isCumulateMonthLmt']:checked").val();

    if(quarterAccumulativeFlag !='' && quarterAccumulativeFlag == '0'){
        if(quarterLimitFlag != '0'){
            commonAlert("请确认季度采购额度已经设定为‘是’!");
            return false;
        }
        if(!(monthlimit == '0' && isCumulateMonthLmt == '0') && !(monthlimit != '0' && isCumulateMonthLmt != '0')){
            commonAlert("季度采购累积能够选择“是”的条件：1.月采购额度为否，月累积为否 2. 月采购额度为“是”，月采购累积为“是”.");
            return false;
        }
    }
    if(isCumulateMonthLmt !='' && isCumulateMonthLmt == '0'){
        if(monthlimit != '0'){
            commonAlert("请确认月采购额度已经设定为‘是’!");
            return false;
        }
    }

    if(quarterLimitFlag !='' && quarterLimitFlag == '0'){
        if(quarterQ1Amt == '' || quarterQ1Amt =='0'){
            commonAlert("Q1季度采购限额不能为空!");
            return false;
        }
        if(quarterQ2Amt == '' || quarterQ2Amt =='0'){
            commonAlert("Q2季度采购限额不能为空!");
            return false;
        }
        if(quarterQ3Amt == '' || quarterQ3Amt =='0'){
            commonAlert("Q3季度采购限额不能为空!");
            return false;
        }
        if(quarterQ4Amt == '' || quarterQ4Amt =='0'){
            commonAlert("Q4季度采购限额不能为空!");
            return false;
        }
    }
    if(yearlyLmtAmt != '' && parseInt(yearlyLmtAmt)>0){
        if(yearlyLmtAmt.length>7){
            commonAlert("年采购限额不能超过7位数!");
            return false;
        }
        var quarterQ1AmtInt = 0;
        var quarterQ2AmtInt = 0;
        var quarterQ3AmtInt = 0;
        var quarterQ4AmtInt = 0;
        if(quarterQ1Amt != '' && quarterQ1Amt!='0'){
            quarterQ1AmtInt = parseInt(quarterQ1Amt);
        }
        if(quarterQ2Amt != '' && quarterQ2Amt!='0'){
            quarterQ2AmtInt = parseInt(quarterQ2Amt);
        }
        if(quarterQ3Amt != '' && quarterQ3Amt!='0'){
            quarterQ3AmtInt = parseInt(quarterQ3Amt);
        }
        if(quarterQ4Amt != '' && quarterQ4Amt!='0'){
            quarterQ4AmtInt = parseInt(quarterQ4Amt);
        }
        if(quarterQ1AmtInt + quarterQ2AmtInt + quarterQ3AmtInt + quarterQ4AmtInt > parseInt(yearlyLmtAmt)){
            commonAlert("四个季度采购额度的金额总和不得大于年度采购额度，请调整您的设置!");
            return false;
        }
    }

	if(monthlyLmtAmt != '' && parseInt(monthlyLmtAmt) > 0){
        if(monthlyLmtAmt.length>7){
            commonAlert("月采购限额不能超过7位数!");
            return false;
        }
    }
    if(quarterQ1Amt != '' && quarterQ1Amt!='0'){
        if(quarterQ1Amt.length>7){
            commonAlert("Q1采购限额不能超过7位数!");
            return false;
        }
        if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
            if(parseInt(monthlyLmtAmt)>parseInt(quarterQ1Amt)){
                commonAlert("Q1采购限额不能小于月采购限额，请调整您的设置");
                return false;
            }
        }
    }
    if(quarterQ2Amt != '' && quarterQ2Amt!='0'){
        if(quarterQ2Amt.length>7){
            commonAlert("Q2采购限额不能超过7位数!");
            return false;
        }
        if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
            if(parseInt(monthlyLmtAmt)>parseInt(quarterQ2Amt)){
                commonAlert("Q2采购限额不能小于月采购限额，请调整您的设置");
                return false;
            }
        }
    }
    if(quarterQ3Amt != '' && quarterQ3Amt!='0'){
        if(quarterQ3Amt.length>7){
            commonAlert("Q3采购限额不能超过7位数!");
            return false;
        }
        if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
            if(parseInt(monthlyLmtAmt)>parseInt(quarterQ3Amt)){
                commonAlert("Q3采购限额不能小于月采购限额，请调整您的设置");
                return false;
            }
        }
    }
    if(quarterQ4Amt != '' && quarterQ4Amt!='0'){
        if(quarterQ4Amt.length>7){
            commonAlert("Q4采购限额不能超过7位数!");
            return false;
        }
        if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
            if(parseInt(monthlyLmtAmt)>parseInt(quarterQ4Amt)){
                commonAlert("Q4采购限额不能小于月采购限额，请调整您的设置");
                return false;
            }
        }
    }



	if(yearlyLmtAmt!='' && monthlyLmtAmt!='' && parseInt(yearlyLmtAmt) >0 && parseInt(monthlyLmtAmt) > 0){
		if(parseInt(monthlyLmtAmt)>parseInt(yearlyLmtAmt)){
			commonAlert("年采购限额不能小于月采购限额，请调整您的设置");
			return false;
		}
		if(monthlyLmtAmt.length>7){
			commonAlert("月采购限额不能超过7位数!");
			return false;
		}
		if(yearlyLmtAmt.length>7){
			commonAlert("年采购限额不能超过7位数!");
			return false;
		}
        if(parseInt(monthlyLmtAmt)*12>parseInt(yearlyLmtAmt)){
            commonAlert("月度采购额度*12不得大于年度的采购额度，请调整您的设置");
            return false;
        }
	}
	
	$("#user_form").find(".lmtAmt").each(function (){
		var temp = $(this).find(".lmtAmtSon").attr("checked");
		if(temp=="checked"){
			var vl = $(this).find("input[type='text']").val();
			if(vl==null || vl==""){
				msg = "请输入相应的‘采购限额’";
				$(this).find("input.w_100").css("borderColor","#FF0033");
				count++;
			}
			if(vl.length>7){
				commonAlert("采购限额不能超过7位数!");
				return false;
			}
		}
	});
	if(count>0){
		commonAlert(msg);
		return;
	}
	
	$("#isAcsRpt").find("input[type='radio']").each(function(){
		if(this.checked){
			count++;
		}
	});
	if(count==0){
		commonAlert("请选择是否‘查看报表’");
		return;
	}else{
		count=0;
	}
	
	$("#isDispRecomprod").find("input[type='radio']").each(function(){
		if(this.checked){
			count++;
		}
	});
	if(count==0){
		commonAlert("请选择是否‘显示推荐商品’");
		return;
	}else{
		count=0;
	}
	
	$("#isDispSalePrmt").find("input[type='radio']").each(function(){
		if(this.checked){
			count++;
		}
	});
	if(count==0){
		commonAlert("请选择是否‘显示促销banner’");
		return;
	}else{
		count=0;
	}
	
	if(count==0)
	{
		var val = $("#topCategoryIds").val();
		$("#product_styles").find(".saleTypeId").each(function(){
			if(this.checked){
				val += this.value;
				val += ",";
			}
		});
		$("#topCategoryIds").val(val);
		
		var goal_options = {
			target : null,
			beforeSubmit : null,
			success : function(data) {
				if(data.result == "500"){
					commonAlert("该用户名已存在，请重新输入");
				}else{
					if(data.result == "updateOk"){
//						reFlahTree(data);
						commonAlert("修改成功!新提交信息将在后台审核之后才能生效.");
						doFormSubmit("search_all", "/costCenter/userList", null, "costRightInfo", null, null);
					}else if(data.result == "insertOk"){
//						reFlahTree(data);
						commonAlert("新增成功!新提交信息将在后台审核之后才能生效.");
						
						ajaxPage('/costCenter/userEditPart/'+data.resultMap.userId,null,null,'costRightInfo');
						/*var before_fn= function (){
							update_cost_user_class('user');
						} ;*/
						//doFormSubmit("search_all", "/costCenter/userList", null, "costRightInfo", null, null);
					}
					else{
						if(data.result==undefined || data.result =='undefined'){
							location.reload();
						}else{
							commonAlert(data.result);
						}
					}
				}

			},
			type : "post"
		};
		
		goal_options.url = url;
		$("form[name='user_form']").ajaxSubmit(goal_options);
	}else{
		commonAlert(msg);
	}
}


function treeDialogToDiv(){
    var diaTree = $.fn.zTree.getZTreeObj("treeDialog");
    var selectText = "";
    var liArrays = "";
    var nodeArray = diaTree.getCheckedNodes(true);
    var choiseCost="";
    for (var i = 0; i < nodeArray.length; i++) {
        selectText = selectText + nodeArray[i].name + "\n";
        liArrays += addUserCost(nodeArray[i].id,nodeArray[i].name);
        // nodeArray[i].id  获取当前ID值
        nodeArray[i].checked = true;
        choiseCost+=nodeArray[i].id+",";
    }
    $("#selectContent").val(selectText);
    $("#costArrayStr").val(choiseCost);
    
    closeDialog("select-costbox");
    $("#costRightInfo").append($('#select-costbox'));
    $("#selectContent.list_cost_center").html(liArrays);
}
function simpleUpdate()
{
	var url="/costCenter/updateUser/"+$(".w_370").text()
	var goal_options = {
			target : null,
			beforeSubmit : null,
			success : function(data) {
				if(data.result == "500"){
					commonAlert("该用户名已存在，请重新输入");
				}else{
					if(data.result == "updateOk"){
//						reFlahTree(data);
						commonAlert("修改成功!新提交信息将在后台审核之后才能生效.");
						doFormSubmit("search_all", "/costCenter/userList", null, "costRightInfo", null, null);
					}else if(data.result == "insertOk"){
//						reFlahTree(data);
						commonAlert("新增成功!新提交信息将在后台审核之后才能生效.");
						
						ajaxPage('/costCenter/userEditPart/'+data.resultMap.userId,null,null,'costRightInfo');
						/*var before_fn= function (){
							update_cost_user_class('user');
						} ;*/
						//doFormSubmit("search_all", "/costCenter/userList", null, "costRightInfo", null, null);
					}
					else{
						if(data.result==undefined || data.result =='undefined'){
							location.reload();
						}else{
							commonAlert(data.result);
						}
					}
				}

			},
			type : "post"
		};
		
		goal_options.url = url;
		$("form[name='user_form']").ajaxSubmit(goal_options);
}


function updateOrSaveUser(url) {
	var new_user_form_data=$('#user_form').serialize()
	if(user_form_data==new_user_form_data){
		commonAlert("用户信息未修改");
		return false;
	}
	var updateFlagStr = $.trim($('#updateFlagStr').val());
	var costArrayStrUpdate = $("#costArrayStrUpdate").val();
	var costArrayStr = $("#costArrayStr").val();
	costArrayStr = replaceall(costArrayStr,',','%2C');
	costArrayStrUpdate = replaceall(costArrayStrUpdate,',','%2C');
	if(new_user_form_data!=user_form_data && new_user_form_data.replace(costArrayStr,'')==user_form_data.replace(costArrayStrUpdate,'')){
		$('#updateFlagStr').val(0);
	}
	
	// var msg = "请填写完整信息 ";
	// var count=0;

	// if($("#userSysName").val()==""){
	// 	commonAlert("请输入‘登录名’");
	// 	count++;
	// 	return;
	// }
	
	// if($("#password").val()==""){
	// 	commonAlert("请输入密码");
	// 	count++;
	// 	return;
	// }
	
	// if($("#password").val().length < 6 || $("#password").val().length > 20){
	// 	commonAlert("请输入密码6~20位!");
	// 	count++;
	// 	return;
	// }
	
	// if($("#confirm_password").val()==""){
	// 	commonAlert("请输入确认密码");
	// 	count++;
	// 	return;
	// }
	// if($("#confirm_password").val().length < 6 || $("#confirm_password").val

	// 		().length > 20){
	// 				commonAlert("请输入确认密码6~20位!");
	// 				count++;
	// 				return;
	// 			}
	
	// if($("#password").val()!=$("#confirm_password").val()){
	// 	commonAlert("两次输入的密码不一致");
	// 	count++;
	// 	return;
	// }
	
	// if($("#userRealName").val()==""){
	// 	commonAlert("请输入‘真实姓名’");
	// 	count++;
	// 	return;
	// }
	
	// if($("#userRealName").val().length>20){
	// 	commonAlert("真实姓名输入字符长度不能超过20 !");
	// 	count++;
	// 	return;
	// }
	
	// if(count==0){
	// 	count++;
	// }else{
	// 	count=0;
	// }
	
	// if($("#cellPhoneNbr").val()=="" && $("#dftPhone1").val()==""){
	// 	commonAlert("请输入‘手机号码’或者‘联系电话1’");
	// 	count++;
	// 	return;
	// }
	
	// if($("#userEmail").val()==""){
	// 	commonAlert("请输入邮箱");
	// 	count++;
	// 	return;
	// }
	
	var costAry = $("#selectContent").find("a");
	if(costAry.length==0){
		commonAlert("请选择‘成本中心’");
		return;
	}
	/*
	if($.trim($("#city_name").val())==""){
		commonAlert("请选择‘配送城市’");
		return;
	}*/
	
	// if($.trim($("#select_escalades").val())==""){
	// 	commonAlert("请选择‘结算单位’");
	// 	return;
	// }
	
	// $("#viewProdStyle").find("input[type='radio']").each(function(){
	// 	if(this.checked){
	// 		count++;
	// 	}
	// });
//	if(count==0){
//		commonAlert("请选择‘商品访问级别’");
//		return;
//	}else{
//		count=0;
//		$("#topCategory").find("input[type='checkbox']").each(function(){
//			if(this.checked){
//				count++;
//			}
//		});
//		if(count==0){
//			commonAlert("请选择‘商品访问范围’");
//			return;
//		}else{
//			count=0;
//		}
//	}
	
	// $("#need_approve").find("input[type='radio']").each(function(){
	// 	if(this.checked){
	// 		count++;
	// 	}
	// });
	// if(count==0){
	// 	commonAlert("请选择‘是否需要审批’");
	// 	return;
	// }else{
	// 	count=0;
	// }
	
	// var approveArrayStr = $.trim($('#approveArrayStr').val());
	// var approveAmt = $.trim($('#approveAmt').val());
	// var approveType = $.trim($('#need_approve input:checked').val())
	// if(approveType==2){
	// 	if(approveArrayStr==''){
	// 		commonAlert("请选择审批人!");
	// 		return false;
	// 	}
	// 	if(approveAmt==''){
	// 		commonAlert("请输入审批金额!");
	// 		return false;
	// 	}
	// 	if(approveAmt.indexOf('.')>=0){
	// 		commonAlert("审批金额必须为整数!");
	// 		return false;
	// 	}
	// 	if(approveAmt.length>7){
	// 		commonAlert("审批金额不能超过7位数!");
	// 		return false;
	// 	}
	// }
	
	// var yearlyLmtAmt = $.trim($("#yearlyLmtAmtTxt").val());
	// var monthlyLmtAmt = $.trim($("#monthlyLmtAmtTxt").val());

 //    var quarterQ1Amt = $.trim($("#quarterQ1Amt").val());
 //    var quarterQ2Amt = $.trim($("#quarterQ2Amt").val());
 //    var quarterQ3Amt = $.trim($("#quarterQ3Amt").val());
 //    var quarterQ4Amt = $.trim($("#quarterQ4Amt").val());

 //    var quarterAccumulativeFlag  = $("input[name='quarterAccumulativeFlag']:checked").val();
 //    var quarterLimitFlag = $.trim($('#quarterLimitFlagChoose').val());
 //    var monthlimit =  $("input[name='monthlimit']:checked").val();
 //    var isCumulateMonthLmt = $("input[name='isCumulateMonthLmt']:checked").val();

 //    if(quarterAccumulativeFlag !='' && quarterAccumulativeFlag == '0'){
 //        if(quarterLimitFlag != '0'){
 //            commonAlert("请确认季度采购额度已经设定为‘是’!");
 //            return false;
 //        }
 //        if(!(monthlimit == '0' && isCumulateMonthLmt == '0') && !(monthlimit != '0' && isCumulateMonthLmt != '0')){
 //            commonAlert("季度采购累积能够选择“是”的条件：1.月采购额度为否，月累积为否 2. 月采购额度为“是”，月采购累积为“是”.");
 //            return false;
 //        }
 //    }
 //    if(isCumulateMonthLmt !='' && isCumulateMonthLmt == '0'){
 //        if(monthlimit != '0'){
 //            commonAlert("请确认月采购额度已经设定为‘是’!");
 //            return false;
 //        }
 //    }

    // if(quarterLimitFlag !='' && quarterLimitFlag == '0'){
    //     if(quarterQ1Amt == '' || quarterQ1Amt =='0'){
    //         commonAlert("Q1季度采购限额不能为空!");
    //         return false;
    //     }
    //     if(quarterQ2Amt == '' || quarterQ2Amt =='0'){
    //         commonAlert("Q2季度采购限额不能为空!");
    //         return false;
    //     }
    //     if(quarterQ3Amt == '' || quarterQ3Amt =='0'){
    //         commonAlert("Q3季度采购限额不能为空!");
    //         return false;
    //     }
    //     if(quarterQ4Amt == '' || quarterQ4Amt =='0'){
    //         commonAlert("Q4季度采购限额不能为空!");
    //         return false;
    //     }
    // }
    // if(yearlyLmtAmt != '' && parseInt(yearlyLmtAmt)>0){
    //      if(yearlyLmtAmt.length>7){
    //          commonAlert("年采购限额不能超过7位数!");
    //          return false;
    //      }
    //     var quarterQ1AmtInt = 0;
    //     var quarterQ2AmtInt = 0;
    //     var quarterQ3AmtInt = 0;
    //     var quarterQ4AmtInt = 0;
    //     if(quarterQ1Amt != '' && quarterQ1Amt!='0'){
    //         quarterQ1AmtInt = parseInt(quarterQ1Amt);
    //     }
    //     if(quarterQ2Amt != '' && quarterQ2Amt!='0'){
    //         quarterQ2AmtInt = parseInt(quarterQ2Amt);
    //     }
    //     if(quarterQ3Amt != '' && quarterQ3Amt!='0'){
    //         quarterQ3AmtInt = parseInt(quarterQ3Amt);
    //     }
    //     if(quarterQ4Amt != '' && quarterQ4Amt!='0'){
    //         quarterQ4AmtInt = parseInt(quarterQ4Amt);
    //     }
    //     if(quarterQ1AmtInt + quarterQ2AmtInt + quarterQ3AmtInt + quarterQ4AmtInt > parseInt(yearlyLmtAmt)){
    //         commonAlert("四个季度采购额度的金额总和不得大于年度采购额度，请调整您的设置!");
    //         return false;
    //     }
    // }

	// if(monthlyLmtAmt != '' && parseInt(monthlyLmtAmt) > 0){
 //        if(monthlyLmtAmt.length>7){
 //            commonAlert("月采购限额不能超过7位数!");
 //            return false;
 //        }
 //    }
    // if(quarterQ1Amt != '' && quarterQ1Amt!='0'){
        // if(quarterQ1Amt.length>7){
        //     commonAlert("Q1采购限额不能超过7位数!");
        //     return false;
        // }
    //     if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
    //         if(parseInt(monthlyLmtAmt)>parseInt(quarterQ1Amt)){
    //             commonAlert("Q1采购限额不能小于月采购限额，请调整您的设置");
    //             return false;
    //         }
    //     }
    // }
    // if(quarterQ2Amt != '' && quarterQ2Amt!='0'){
        // if(quarterQ2Amt.length>7){
        //     commonAlert("Q2采购限额不能超过7位数!");
        //     return false;
        // }
    //     if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
    //         if(parseInt(monthlyLmtAmt)>parseInt(quarterQ2Amt)){
    //             commonAlert("Q2采购限额不能小于月采购限额，请调整您的设置");
    //             return false;
    //         }
    //     }
    // }
    // if(quarterQ3Amt != '' && quarterQ3Amt!='0'){
        // if(quarterQ3Amt.length>7){
        //     commonAlert("Q3采购限额不能超过7位数!");
        //     return false;
        // }
    //     if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
    //         if(parseInt(monthlyLmtAmt)>parseInt(quarterQ3Amt)){
    //             commonAlert("Q3采购限额不能小于月采购限额，请调整您的设置");
    //             return false;
    //         }
    //     }
    // }
    // if(quarterQ4Amt != '' && quarterQ4Amt!='0'){
        // if(quarterQ4Amt.length>7){
        //     commonAlert("Q4采购限额不能超过7位数!");
        //     return false;
        // }
    //     if(monthlyLmtAmt != '' && monthlyLmtAmt!='0'){
    //         if(parseInt(monthlyLmtAmt)>parseInt(quarterQ4Amt)){
    //             commonAlert("Q4采购限额不能小于月采购限额，请调整您的设置");
    //             return false;
    //         }
    //     }
    // }



	// if(yearlyLmtAmt!='' && monthlyLmtAmt!='' && parseInt(yearlyLmtAmt) >0 && parseInt(monthlyLmtAmt) > 0){
	// 	if(parseInt(monthlyLmtAmt)>parseInt(yearlyLmtAmt)){
	// 		commonAlert("年采购限额不能小于月采购限额，请调整您的设置");
	// 		return false;
	// 	}
		// if(monthlyLmtAmt.length>7){
		// 	commonAlert("月采购限额不能超过7位数!");
		// 	return false;
		// }
		// if(yearlyLmtAmt.length>7){
		// 	commonAlert("年采购限额不能超过7位数!");
		// 	return false;
		// }
 //        if(parseInt(monthlyLmtAmt)*12>parseInt(yearlyLmtAmt)){
 //            commonAlert("月度采购额度*12不得大于年度的采购额度，请调整您的设置");
 //            return false;
 //        }
	// }
	
	// $("#user_form").find(".lmtAmt").each(function (){
	// 	var temp = $(this).find(".lmtAmtSon").attr("checked");
	// 	if(temp=="checked"){
	// 		var vl = $(this).find("input[type='text']").val();
	// 		if(vl==null || vl==""){
	// 			msg = "请输入相应的‘采购限额’";
	// 			$(this).find("input.w_100").css("borderColor","#FF0033");
	// 			count++;
	// 		}
			// if(vl.length>7){
			// 	commonAlert("采购限额不能超过7位数!");
			// 	return false;
	// 		}
	// 	}
	// });
	// if(count>0){
	// 	commonAlert(msg);
	// 	return;
	// }
	
	// $("#isAcsRpt").find("input[type='radio']").each(function(){
	// 	if(this.checked){
	// 		count++;
	// 	}
	// });
	// if(count==0){
	// 	commonAlert("请选择是否‘查看报表’");
	// 	return;
	// }else{
	// 	count=0;
	// }
	
	// $("#isDispRecomprod").find("input[type='radio']").each(function(){
	// 	if(this.checked){
	// 		count++;
	// 	}
	// });
	// if(count==0){
	// 	commonAlert("请选择是否‘显示推荐商品’");
	// 	return;
	// }else{
	// 	count=0;
	// }
	
	// $("#isDispSalePrmt").find("input[type='radio']").each(function(){
	// 	if(this.checked){
	// 		count++;
	// 	}
	// });
	// if(count==0){
	// 	commonAlert("请选择是否‘显示促销banner’");
	// 	return;
	// }else{
	// 	count=0;
	// }
	
	if(count==0)
	{
		var val = $("#topCategoryIds").val();
		$("#product_styles").find(".saleTypeId").each(function(){
			if(this.checked){
				val += this.value;
				val += ",";
			}
		});
		$("#topCategoryIds").val(val);
		
		var goal_options = {
			target : null,
			beforeSubmit : null,
			success : function(data) {
				if(data.result == "500"){
					commonAlert("该用户名已存在，请重新输入");
				}else{
					if(data.result == "updateOk"){
//						reFlahTree(data);
						commonAlert("修改成功!新提交信息将在后台审核之后才能生效.");
						//doFormSubmit("search_all", "/costCenter/userList", null, "costRightInfo", null, null);
					}else if(data.result == "insertOk"){
//						reFlahTree(data);
						commonAlert("新增成功!新提交信息将在后台审核之后才能生效.");
						
						ajaxPage('/costCenter/userEditPart/'+data.resultMap.userId,null,null,'costRightInfo');
						/*var before_fn= function (){
							update_cost_user_class('user');
						} ;*/
						//doFormSubmit("search_all", "/costCenter/userList", null, "costRightInfo", null, null);
					}
					else{
						if(data.result==undefined || data.result =='undefined'){
							location.reload();
						}else{
							commonAlert(data.result);
						}
					}
				}

			},
			type : "post"
		};
		
		goal_options.url = url;
		$("form[name='user_form']").ajaxSubmit(goal_options);
	}else{
		commonAlert(msg);
	}