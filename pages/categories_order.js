function compareFn(a, b) {
  if (a == "Autres" || b == "Sponsors"){
    return -1;
  }
  if (a == "Sponsors" || b == "Autres"){
    return 1;
  }
  return a.localeCompare(b.name);
}