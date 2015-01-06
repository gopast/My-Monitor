 var SockClient = function (monitorType) {
        var self = this;
        self.monitorType = (monitorType || 'follow').toLowerCase();
        self.follow_req_chan = 'follow-request';
        self.follow_resp_chan = 'follow-response';
        self.tail_resp_chan = 'tail-response';
        self.tail_req_chan = 'tail-request';
        self.namespace = '/monitor';
        self.server_uri = 'http://' + window.location.host + self.namespace;
        self.socket = io.connect(self.server_uri);

        //wrap
        self.emit = function (chan, data) {
            self.socket.emit(chan, data);
        };

        //connect
        self.socket.on("connect-response", function (msg) {
            if (msg.data == 'Connected') {
                var tip = 'Connected to ' + self.server_uri + '</br>';
                $('#connect-status').html(tip);
            }
        });
        //follow
        self.socket.on(self.follow_resp_chan, function (msg) {
            console.log(msg);
            if (msg.pos == 0) {
                setTimeout(function () {
                    self.emit(self.follow_req_chan, {data: $("#tail-pos").val()});
                }, 2000);
            } else {
                $("#tail-pos").val(msg.pos);
                console.log(msg);
                var tip=msg.data||"服务器很安静，没有新的动态...";
                $('#log').append('Received: ' +tip + '</br>');
            }
        });
        //tail
        self.socket.on(self.tail_resp_chan, function (msg) {
            if (msg.data) {
                $('#log').append('Received: ' + msg.data + '</br>');
            }
        });

        self.init=function(){
            if(self.monitorType=='tail'){
               $("#show-tail").on("click",function(){
                   $('#log').empty();
                   self.startTail();
               });
               $(document).on('keypress',function(e){
                    if(e.keyCode==13){
                        $("#show-tail").click();
                    }
               });
            }
           
            return self;
        };

        self.start = function () {
            if (self.monitorType == 'follow') {
                self.startFollow();
            } else if (self.monitorType == 'tail') {
                //self.startTail();
            }
        };
        self.startFollow = function () {
            setInterval(function () {
                var data = {data: $("#tail-pos").val()};
                self.emit(self.follow_req_chan, data);
                self.log(self.follow_req_chan,data);
            }, 2000);
        };
        self.startTail = function () {
            var data= {lines: $("#line-count").val(),key:$("#key-text").val()};
            self.emit(self.tail_req_chan, data);
            self.log(self.tail_req_chan,data);
        };

        self.log=function(chan,data){
            var msg="client sending message ("+chan+")... :";
            console.log(msg);
            console.log(data);
        };

};
