var apiRoot = 'https://gae-starterpack-2.appspot.com/_ah/api';
var currentKey = ''

loadNextCode = function() {
    $('#codeblob').empty()
    gapi.client.hackerorslacker.codeentry.list().execute(function (response) {
	escaped_code=response.entries[0].code_blob;
	currentKey = response.entries[0].key;
	//	    escaped_code=$('<div/>').text(code).html();
	//escaped_code=code.replace(/[\r\n]/g, "<br />");
	$('#codeblob').append(escaped_code);
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

upvote = function() {
    $('#codeblob').hide()
    $('#spinner').show()
    $('.vote-btn').addClass('disabled')
    gapi.client.hackerorslacker.codeentry.up({'id': currentKey}).execute(function (response) {
	loadNextCode()
    });
}

downvote = function() {
    $('#codeblob').hide()
    $('#spinner').show()
    $('.vote-btn').addClass('disabled')
    gapi.client.hackerorslacker.codeentry.down({'id': currentKey}).execute(function (response) {
	loadNextCode()
    });
}

ignorevote = function() {
    $('#codeblob').hide()
    $('#spinner').show()
    $('.vote-btn').addClass('disabled')
    gapi.client.hackerorslacker.codeentry.ignore({'id': currentKey}).execute(function (response) {
	loadNextCode()
    });
}

init = function() {
    gapi.client.load('hackerorslacker', 'v1', loadNextCode,apiRoot);
}

submit_init = function() {
    gapi.client.load('hackerorslacker', 'v1', loadNextSubmitCode,apiRoot);
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
