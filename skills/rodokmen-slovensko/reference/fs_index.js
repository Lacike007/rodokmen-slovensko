// Vyhľadávanie v indexe FamilySearch z prihlásenej karty (javascript_tool).
// Parametre: q.surname, q.givenName, q.anyPlace, q.anyDate.from/to, q.birthLikeDate.from/to,
//            f.collectionId=1554443 (slovenské cirkevné knihy), count (max 100), offset.
// Výsledok sa uloží do window.out; vypisuj po častiach (výstup nástroja sa reže).
const fsHladaj = async (params) => {
  const r = await fetch('https://www.familysearch.org/service/search/hr/v2/personas?' + params + '&count=100',
    { headers: { accept: 'application/json' }, credentials: 'include' });
  if (!r.ok) return ['HTTP ' + r.status];
  const j = await r.json();
  return (j.entries || []).map(e => {
    const p = e.content.gedcomx.persons;
    const meno = x => x.names?.[0]?.nameForms?.[0]?.fullText;
    const hlavna = p.find(x => x.principal) || p[0];
    const fakty = (hlavna.facts || []).map(f => (f.type || '').split('/').pop() + ':' +
      (f.date?.original || '') + ' ' + (f.place?.original || '')).join('; ');
    const ostatni = p.filter(x => x !== hlavna).map(meno).join(', ');
    return meno(hlavna) + ' | ' + fakty + ' | ' + ostatni + ' | ' + e.id;
  });
};
// Príklad: Novákovci v Bardejove 1875–1905
window.out = (await fsHladaj('q.surname=Nov%C3%A1k&q.anyPlace=Bardejov&q.anyDate.from=1875&q.anyDate.to=1905'))
  .filter(s => /Bardejov|B[aá]rtfa/i.test(s));
window.out.join('\n');
