var apiRoot = 'https://gae-starterpack-2.appspot.com/_ah/api';
var currentKey = ''

function wordwrap( str, width, brk, cut ) {
    brk = brk || '\n';
    width = width || 75;
    cut = cut || false;
    if (!str) { return str; }
    var regex = '.{1,' +width+ '}(\\s|$)' + (cut ? '|.{' +width+ '}|.+$' : '|\\S+?(\\s|$)');

    return str.match( RegExp(regex, 'g') ).join( brk );
}

loadNextCode = function() {
    $('#codeblob').empty()

    gapi.client.hackerorslacker.codeentry.list().execute(function (response) {
	escaped_code=response.entries[0].code_blob;
	currentKey = response.entries[0].key;
	//	    escaped_code=$('<div/>').text(code).html();
	//escaped_code=code.replace(/[\r\n]/g, "<br />");
	$('#codeblob').append(wordwrap(escaped_code, 30, "\n", false));
	SyntaxHighlighter.all()
	$('#spinner').hide()
	$('#codeblob').show()
	$('.vote-btn').removeClass('disabled')
	
    });
}

loadNextSubmitCode = function() {
    $('#spinner').hide()
    $('#submit-btn').show()
}

loadNextScoreCode = function() {
}

upvote = function() {
    $('#codeblob').hide()
    $('#spinner').show()
    $('.vote-btn').addClass('disabled')
    gapi.client.hackerorslacker.codeentry.up({'id': currentKey}).execute(function (response) {
	$('#previous-author').text(response['result']['git_username'])
	$('#previous-score').text(response['result']['score'])
	$('#previous-stats').show()
	loadNextCode()
    });
}

downvote = function() {
    $('#codeblob').hide()
    $('#spinner').show()
    $('.vote-btn').addClass('disabled')
    gapi.client.hackerorslacker.codeentry.down({'id': currentKey}).execute(function (response) {
	$('#previous-author').text(response['result']['git_username'])
	$('#previous-score').text(response['result']['score'])
	$('#previous-stats').show()
	loadNextCode()
    });
}

ignorevote = function() {
    $('#codeblob').hide()
    $('#spinner').show()
    $('.vote-btn').addClass('disabled')
    gapi.client.hackerorslacker.codeentry.ignore({'id': currentKey}).execute(function (response) {
	$('#previous-author').text(response['result']['git_username'])
	$('#previous-score').text(response['result']['score'])
	$('#previous-stats').show()
	loadNextCode()
    });
}

init = function() {
    gapi.client.load('hackerorslacker', 'v1', loadNextCode,apiRoot);
}

submit_init = function() {
    gapi.client.load('hackerorslacker', 'v1', loadNextSubmitCode,apiRoot);
}

score_init = function() {
    gapi.client.load('hackerorslacker', 'v1', loadNextScoreCode,apiRoot);
}

do_submit = function() {
    $('#spinner').show();
    $('#submit-btn').addClass('disabled');
    test=$('#code_blob').val();
    gapi.client.hackerorslacker.codeentry.add(
	{'code_blob': test,
	 'language': $('#language').val(),
	 'git_username': $('#git_username').val()}).execute( function (response) {
	     $('#spinner').hide()
	     $('#submit-msg').show()
	     $('#submit-btn').removeClass('disabled')
	 });
}
