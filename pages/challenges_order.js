function compareFn(a, b) {
    const difficultyOrder = ["Très Facile", "Facile", "Moyen", "Difficile", "Très Difficile"];
    
    const fixed_order_osint = ["Un appel étrange...","Où va Eduardo O'Sullivan","Un homme occupé","La langue à son chat","Vole petit oiseau","Une escapade odorante","Libérez-moi !"];
    const fixed_order_hardware = ["Odobenus rosmarus","Changement de canal","BreizhBoot (1/3)","BreizhBoot (2/3)","BreizhBoot (3/3)"];

    // Check if names are in the fixed order list
    var indexA = fixed_order_osint.indexOf(a.name);
    var indexB = fixed_order_osint.indexOf(b.name);

    if (indexA == -1 && indexB == -1) {
        indexA = fixed_order_hardware.indexOf(a.name);
        indexB = fixed_order_hardware.indexOf(b.name);
    }
  
    if (indexA !== -1 && indexB !== -1) {
      // Both are in the fixed order list, compare by their positions
      return indexA - indexB;
    } else if (indexA !== -1) {
      // Only a is in the fixed order list, it should come first
      return -1;
    } else if (indexB !== -1) {
      // Only b is in the fixed order list, it should come first
      return 1;
    }

  // Compare by difficulty
  const diffA = difficultyOrder.indexOf(a.tags[0].value);
  const diffB = difficultyOrder.indexOf(b.tags[0].value);
  if (diffA !== diffB) return diffA - diffB;

  // Compare by number of solves (higher solves come first)
  if (a.solves !== b.solves) return b.solves - a.solves;

  // Compare by name
  return a.name.localeCompare(b.name);
}