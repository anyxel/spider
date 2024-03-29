// Octal codes are not allowed in strict mode.
// Hence the hexadecimal escape sequence
const TermColors = {
  Red: "\x1B[1;31m",
  Green: "\x1B[1;32m",
  Purple: "\x1B[1;35m",
  Reset: "\x1B[0m",
};

let command = '';
let curr_line = '';
const SHELL_PROMPT = TermColors.Purple + "spider@anyxel:~$ " + TermColors.Reset;

const term = new Terminal({
  rows: 30,
  cursorBlink: true,
  rendererType: 'canvas',
  screenReaderMode: true,
  fontSize: 16,
  tabStopWidth: 4,
});

let terminalContainer = document.getElementById('terminal');
term.open(terminalContainer);

term.prompt = function () {
  term.write('\r\n$ ');
};

term.writeln('Welcome to ' + '\x1b[1;33m' + 'Spider' + '\x1b[37m' + ' Terminal');
term.writeln('');
term.write(SHELL_PROMPT);
term.prompt();

term.onData(e => {
  switch (e) {
    case '\u0003': // Ctrl+C
      command = '';
      curr_line = '';
      term.clear();
      break;
    case '\r': // Enter

      if (curr_line.replace(/^\s+|\s+$/g, '').length !== 0) { // Check if string is all whitespace
        entries.push(curr_line);
        currPos = entries.length - 1;
      } else {
        runCommand(term, command);
        command = '';
      }
      curr_line = '';
      term.prompt();

      break;
    case '\u007F': // Backspace (DEL)
      // Do not delete the prompt
      if (term._core.buffer.x > 2) {
        term.write('\b \b');
        if (command.length > 0) {
          command = command.substr(0, command.length - 1);
        }
      }
      break;
    default: // Print all other characters for demo
      if (e >= String.fromCharCode(0x20) && e <= String.fromCharCode(0x7E) || e >= '\u00a0') {
        command += e;
      }
  }
});

term.onKey((e) => {
  const ev = e.domEvent;
  const printable = !ev.altKey && !ev.ctrlKey && !ev.metaKey;

  if (ev.keyCode === 13) {
  } else if (ev.keyCode === 8) {
    // Do not delete the prompt
    if (term._core.buffer.x > 2) {
      term.write('\b \b');
    }
  } else if (ev.ctrlKey && ev.key === 'l') {
    command = '';
    curr_line = '';
    term.clear();
  } else if (ev.ctrlKey && ev.key === 'c') {
  } else if (printable) {
    term.write(e.key);
  }
});

webSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const message = data['message'];

  term.write(message);
};
