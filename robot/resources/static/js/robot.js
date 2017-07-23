var socket = null;

function send_command(cmd, args) {
  socket.send(JSON.stringify({
    "type": cmd,
    "args": args
  }));
};

function forward(val) {
  send_command('move_fwd', {});
  return false;
}

function back(val) {
  send_command('move_fwd', {});
  return false;
}

function start_robot() {
  var loc = new URI(document.location);
  var host = loc.hostname();

  socket = new WebSocket(sprintf('ws://%s:8082/', host));

  socket.onopen = function (event) {
      setRealtime();
  };

  socket.onmessage = function (event) {
    // Parse JSON message and dispatch to processor functions
    var msg = JSON.parse(event.data);
    switch (msg.type) {
      case "video":
        video(msg.payload)
        break;
    }
  };

  var lastKey = 0;

  $(document).keyup(function(event) {
    send_command('stop', {});
    console.log("HALT");
    lastKey = 0;
  });

  $(document).keydown(function(event) {
    if (lastKey == 0) {
      switch (event.which) {
        case 87:
          // W
          send_command('move_fwd', {});
          lastKey = event.which;
          break;
        case 83:
          // S
          send_command('move_back', {});
          lastKey = event.which;
          break;
        case 65:
          // A
          send_command('move_left', {});
          lastKey = event.which;
          break;
        case 68:
          // D
          send_command('move_right', {});
          lastKey = event.which;
          break;

        case 76:
          // L
          send_command('arm_right', {});
          lastKey = event.which;
          break;

        case 74:
          // J
          send_command('arm_left', {});
          lastKey = event.which;
          break;

        case 73:
          // I
          send_command('arm_extend', {});
          lastKey = event.which;
          break;

        case 75:
          // K
          send_command('arm_retract', {});
          lastKey = event.which;
          break;

        case 89:
          // Y
          send_command('arm_up', {});
          lastKey = event.which;
          break;

        case 72:
          // H
          send_command('arm_down', {});
          lastKey = event.which;
          break;

        case 85:
          // U
          send_command('arm_close', {});
          lastKey = event.which;
          break;

        case 79:
          // O
          send_command('arm_open', {});
          lastKey = event.which;
          break;

      }
      console.log(event.which);
    }
  });
};
