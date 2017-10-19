see3d_dom.setOption(option = {
        tooltip: {},
        backgroundColor: 'hsla(0,%100,50%,0)',
        title:{
                text:"AR Ageing By Month",
                subtext:"You can rotate to get a better angle, Scroll to zoom,first 10 days are not included",
                textStyle:{
                    color:'#FFF',
                }
            },
        xAxis3D: {
            name:"Time",
            type: 'category',
            data:{{cols|safe}},
            axisLine:{lineStyle:{color:"#71EFFD"}},
        },
        yAxis3D: {
            type: 'category',
            name:'Ageing',
            data:{{indices|safe}},
            axisLine:{lineStyle:{color:"#71EFFD"}},
        },
        zAxis3D: {
            type: 'value',
            name:'Amount in RMB',
            axisLine:{lineStyle:{color:"#71EFFD"}},
            // min: 0,
            // max: 100000
        },
        grid3D: {
            viewControl: {
                alpha: 10,
                beta: 100,
                distance:200,
            },
            postEffect: {
                enable: true,
                SSAO: {
                    enable: true
                },

                bloom:{enable:true,}
            },
            axisTick:
                {
                interval:0},
            splitLine:{
                show:false,
            },
            boxHight:500,
            boxWidth:10*{{col_len}},
            boxDepth:300,
            light: {
                main: {
                    shadow: true,
                    intensity: 2
                },
            },
        },
        series: [{
            coordinateSystem:'cartesian3D',
            type: 'bar3D',
            shading: 'realistic',
            barSize: 9,
            wireframe: {
                show: false
            },
            label:{show:false},
            emphasis:{label:{show:false,}},
            bevelSize:1,
            bevelSmoothness:1,
            data: {{data|safe}},
        }]
    });
see3d_dom.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(234);
});