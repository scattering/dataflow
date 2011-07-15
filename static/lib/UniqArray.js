function makeUnique(array) {
	var a = [];
	var l = array.length;
	for (var i=0; i<l; i++) {
		for (var j=i+1; j<l; j++) {
			if (array[i] === array[j])
				j = ++i;
			}
		a.push(array[i]);
	}
	return a;
};

