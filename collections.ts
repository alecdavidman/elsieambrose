import works from './works.json';
export const collections = [
 {slug:'paintings',title:'Paintings',plates:['016','004','015','026','013','017','028'],cover:'/artwork/plate-037.jpeg'},
 {slug:'drawings',title:'Drawings',plates:['027','005','001','002','006','007','008','009','010','011','012','018','019','020','021','022','023','024'],cover:'/artwork/plate-055.jpeg'},
 {slug:'sculptures',title:'Sculptures',plates:['003','014','025'],cover:'/artwork/plate-002.jpeg'},
].map(collection=>({...collection,items:collection.plates.flatMap(plate=>{const work=works.find(w=>w.plate===plate)!;return work.images.map((image,view)=>({...image,title:work.title,description:work.description,plate,view:view+1,totalViews:work.images.length}));})}));
export type Collection = typeof collections[number];
