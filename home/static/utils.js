Array.prototype.getLastItem = function() {
    if(this.length == 0)
        return null;
    return this[this.length-1];
}

Array.prototype.clone = function() {
	return this.slice(0);
};

function getHashPath() {
    return window.location.hash.substr(1).split("/");
}

function getPath() {
    var path = [];
    window.location.pathname.split("/").forEach(function(d) {
        if(d) path.push(d);
    });
    return path;
}