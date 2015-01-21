$("pre code").addClass("language-python");

String.prototype.endsWith = function(suffix){
  return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

$('a').each(function(){
  var x=this.href;

  if (this.href.endsWith('/'))
    this.href = this.href + "index.html";
});
