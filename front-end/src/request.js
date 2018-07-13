function getTxn(height) {
    $('.blockheight').append(height);
    $('#txn table tbody').empty();
    var data = txn[height];
    for (var i in data){
        if (data[i].type=='tx'||data[i].type=='call'){
            $('#txn table tbody').append('<tr>' +
                    '<td>'+data[i].tx_hash+'</td>' +
                    '<td>'+data[i].type+'</td>' +
                    '<td>'+data[i].from+'</td>' +
                    '<td>'+data[i].to+'</td>' +
                    '<td>'+data[i].amount+'</td>' +
                    '<td>'+data[i].comment+'</td>' +
                    '</tr>')
        }
    }
}
function transfer() {
    $('.transfer').addClass('disabled');
    var from = $('#transfer input').eq(0).val();
    var to = $('#transfer input').eq(1).val();
    var amount = $('#transfer input').eq(2).val();
    var reg = /^[0-9a-f]{64}$/;
    if (!reg.test(to)){
        alert('Please fill in the correct address!');
        $('.transfer').removeClass('disabled');
        return
    }
    if (amount<=0){
        alert('Amount cannot be less than 0');
        $('.transfer').removeClass('disabled');
        return
    }
    if (amount>mineramount){
        alert('Insufficient balance!');
        $('.transfer').removeClass('disabled');
        return
    }
    var parma = {
        'nonce': 0,
        'from': from,
        'type': 'tx',
        'to': to,
        'amount': amount
    }
    $.ajax({
        url:'/txion',
        type: 'POST',
        data: JSON.stringify(parma),
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
            if(data.msg=='ok'){
                $('.msg').show();
                setTimeout(function(){
                    $('.msg').hide();
                    $('#transfer').modal('hide');
                    $('.transfer').removeClass('disabled');
                }, 1000)
            }
        }
    })
}
function getInput(x){
    input = x;
}
function getModel(x){
    $.model = x;
}
function upload() {
    var formdata = new FormData();
    formdata.append('file', $('#imgInputUpload')[0].files[0]);
    var parma = {
        type: 'input_data',
        'author': $.mineraddr
    };
    formdata.append('json', 
            new Blob([JSON.stringify(parma)], { "type": "application/json"})
            )
        $.ajax({
            url: 'http://192.168.5.11:5000/txion',
            beforeSend: function(request) {
                request.setRequestHeader("Access-Control-Allow-Origin", "*")
            },
            type: 'POST',
            data: formdata,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data){
                console.log(data)
                getInputData()
            }
        })
}
function list_input(cb) {
    var formdata = new FormData();
    var parma = {
        type: 'list_input',
        'author': $.mineraddr
    };
    formdata.append('json', 
            new Blob([JSON.stringify(parma)], { "type": "application/json"})
            )
        $.ajax({
            url: 'http://192.168.5.11:5000/txion',
            beforeSend: function(request) {
                request.setRequestHeader("Access-Control-Allow-Origin", "*")
            },
            type: 'POST',
            data: formdata,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data){
                cb(data)
            }
        })
}
function call() {
    $('.call').addClass('disabled');
    var formdata = new FormData();
    formdata.append('file', $('#imgInput')[0].files[0]);
    if (!$("#imgInput").val()) {
        alert('Please upload the image!');
        $('.call').removeClass('disabled');
        return
    }
    if ($('#imgInput')[0].files[0].size > (200*1024)) {
        alert('Image size cannot exceed 200K!');
        $('.call').removeClass('disabled');
        return
    }
    var parma = {
        from: $.mineraddr,
        to: 'DefaultContract',
        //input: formdata,
        model: $.model,
        type: 'call',
        nonce: 0
    };
    formdata.append('parma', JSON.stringify(parma));
    $.ajax({
        url: '/txion',
        type: 'POST',
        data: formdata,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data){
            if(data.msg=='ok'){
                $('.msg').show();
                setTimeout(function(){
                    $('.msg').hide();
                    $('#call').modal('hide');
                    $('.call').removeClass('disabled');
                }, 1000)
            }else{
                alert(data.info);
                $('.call').removeClass('disabled');
            }
        }
    })
}

function getBlocks() {
    $.get('/'+blockurl, function (data) {
        if (data) {
            $('.mineramount').html(data.account);
            $.mineramount = data.account;
            $('#blocks table tbody').empty();
            for (var i =0;i<data.block.length;i++) {
                if (data.block[i].data.length>0){
                    data.block[i].data.length = data.block[i].data.length-1;
                }
                $('#blocks table tbody').append('<tr>' +
                        '<td><a href="#" data-toggle="modal" data-target="#txn" onclick="getTxn('+data.block[i].index+')">'+data.block[i].index+'</a></td>' +
                        '<td>'+new Date(data.block[i].timestamp)+'</td>' +
                        '<td>0x0000000000000000000000000000000000000000001</td>' +
                        '<td>'+data.block[i].data.length+'</td>' +
                        '<td>5</td>' +
                        '</tr>');
                txn[data.block[i].index] = data.block[i].data;
            }
        }
    })
}

function getInputData() {
    list_input(function(data) {
        if (data['msg'] == 'ok') {
            var records_dict = data['info'];
            $('#inputs table tbody').empty();
            for (var addr in records_dict ) {
                var record = records_dict[addr];
                $('#inputs  table tbody').append(
                        '<tr>' +
                        '<td>' + addr + '</td>' +
                        '<td>' + JSON.stringify(records_dict[addr]) + '</td>' +
                        '</tr>'
                );
            }
        }
        else {
            console.log(data)
        }

    });
}

$(document).ready(function() {
    $('body').css('min-height', window.innerHeight);
    if ($.mineraddr) {
        $('.mineraddr').html($.mineraddr);
        blockurl = 'getBlock?address=' + $.mineraddr;
    }else {
        blockurl = 'getBlock';
    }
    var txn = {};
    getBlocks(); setInterval(function () { getBlocks(); }, 15000);
    getInputData(); setInterval(function () { getInputData(); }, 5000);
})

