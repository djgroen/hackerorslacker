var apiRoot = 'https://gae-starterpack-2.appspot.com/_ah/api';
var currentKey = ''

loadNextCode = function() {
    $('#codeblob').empty()
    gapi.client.hackerorslacker.codeentry.list().execute(function (response) {
	code=response.entries[0].code_blob;
	currentKey = response.entries[0].key;
	//	    escaped_code=$('<div/>').text(code).html();
	escaped_code=code.replace(/[\r\n]/g, "<br />");
	$('#codeblob').append(escaped_code);
	$('#spinner').hide()
	$('#codeblob').show()
	$('.vote-btn').removeClass('disabled')
//	    Rainbow.color(escaped_code, 'C++', function (hilited_code) {
//		$('#codeblob').append(hilited_code);
//	    });
    });
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
